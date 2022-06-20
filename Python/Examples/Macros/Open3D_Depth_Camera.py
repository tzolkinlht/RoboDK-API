# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
#
# This example shows how to retrieve and display the point cloud from the 32-bit depth map of a simulated camera.
# It uses Open3D for converting the depth map to a 3D mesh and for vizualisation.
# Left-click the view to move the mesh in the viewer.

from robodk.robolink import *
from tempfile import TemporaryDirectory
import numpy as np
import open3d as o3d

#----------------------------------
# Get the simulated camera from RoboDK
RDK = Robolink()

cam_item = RDK.Item('Depth Camera', ITEM_TYPE_CAMERA)
if not cam_item.Valid():
    cam_item = RDK.Cam2D_Add(RDK.ActiveStation(), 'DEPTH')
    cam_item.setName('Depth Camera')
cam_item.setParam('Open', 1)


#----------------------------------
# Retrieve camera settings / camera matrix
def settings_to_dict(settings):
    if not settings:
        return {}

    settings_dict = {}
    settings_list = [setting.split('=') for setting in settings.strip().split(' ')]
    for setting in settings_list:
        key = setting[0].upper()
        val = setting[-1]

        if key in ['FOV', 'PIXELSIZE', 'FOCAL_LENGTH', 'FAR_LENGTH']:
            val = float(val)
        elif key in ['SIZE', 'ACTUALSIZE', 'SNAPSHOT']:
            w, h = val.split('x')
            val = (int(w), int(h))
        elif key == val.upper():
            val = True  # Flag

        settings_dict[key] = val

    return settings_dict


cam_settings = settings_to_dict(cam_item.setParam('Settings'))
w, h = cam_settings['SIZE']
fy = h / (2 * np.tan(np.radians(cam_settings['FOV']) / 2))
cam_mtx = o3d.camera.PinholeCameraIntrinsic(width=w, height=h, fx=fy, fy=fy, cx=w / 2, cy=h / 2)
cam_pose = cam_item.getLink(ITEM_TYPE_FRAME).Pose()

#----------------------------------------------
# Get the depth map

# Method 1: by socket (requires RoboDK v5.4.3-2022-06-20)
depth32_socket = None
bytes_img = RDK.Cam2D_Snapshot("", cam_item, 'DEPTH')
if isinstance(bytes_img, bytes) and bytes_img != b'':
    # By socket
    depth32_socket = np.frombuffer(bytes_img, dtype='>u4')
    w, h = depth32_socket[:2]
    depth32_socket = np.flipud(np.reshape(depth32_socket[2:], (h, w))).astype(np.uint32)

# Method 2: from disk
depth32_disk = None
with TemporaryDirectory(prefix='robodk_') as td:
    tf = td + '/temp.grey32'
    if RDK.Cam2D_Snapshot(tf, cam_item, 'DEPTH') == 1:
        depth32_disk = np.fromfile(tf, dtype='>u4')
        w, h = depth32_disk[:2]
        depth32_disk = np.flipud(np.reshape(depth32_disk[2:], (h, w))).astype(np.uint32)

# Scale it
depth = (depth32_socket / np.iinfo(np.uint32).max) * cam_settings['FAR_LENGTH']
depth = depth.astype(np.uint16)

#----------------------------------------------
# Convert to point cloud, approximate mesh
pcd = o3d.geometry.PointCloud.create_from_depth_image(o3d.geometry.Image(depth), cam_mtx)
pcd.estimate_normals()
pcd.orient_normals_consistent_tangent_plane(100)

mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
vertices_to_remove = densities < np.quantile(densities, 0.05)
mesh_poisson.remove_vertices_by_mask(vertices_to_remove)

#----------------------------------------------
# Show it to the world!
o3d.visualization.draw_geometries([pcd, mesh_poisson], mesh_show_back_face=True, mesh_show_wireframe=True)

#----------------------------------------------
# Import the mesh into RoboDK
with TemporaryDirectory(prefix='robodk_') as td:
    tf = td + '/mesh.ply'
    o3d.io.write_triangle_mesh(tf, mesh_poisson, write_ascii=True)
    mesh_item = RDK.AddFile(tf)

mesh_item.setPose(cam_pose)
mesh_item.setColor([0, 0, 1, 0.75])
