RoboDK API
===========

This repository is the implementation of the RoboDK API in different programming languages for simulation and offline programming.
The RoboDK API allows you to program any industrial robot arm using your preferred programming language.

The RoboDK API is available in the following programming languages:
* [Python](https://pypi.python.org/pypi/robodk/)
* [C#](./C%23)
* [Matlab](https://www.mathworks.com/matlabcentral/fileexchange/65690-robodk-api-for-matlab)
* [C++](https://robodk.com/doc/en/CppAPI/index.html)
* [Visual Basic](./Visual%20Basic)

The RoboDK API allows creating simulations for industrial robots, specific mechanisms and generating vendor-specific programs for robots.
With the RoboDK API it is possible to simulate and program any industrial robot using your preferred programming language.
The RoboDK API provides an alternative to using vendor-specific programming languages.

While RoboDK's graphical user interface can be used to create programs, it is possible to extend the robot controller limitations by using a universal programming language such as Python.
The following page provides an overview of the RoboDK API using Python: <https://robodk.com/offline-programming>.

RoboDK can be used for a wide range of robot manufacturing applications, such as robot machining, 3D printing, synchronizing multiple robots, pick and place, and so on.
 * [Industrial Robot application examples](https://robodk.com/stations)
 * [Robot library](https://robodk.com/library)
 * [RoboDK Blog](https://robodk.com/blog/)
 * [RoboDK Forum](https://robodk.com/forum/)

**Important:** The RoboDK API is not the same as the [RoboDK Plug-In interface](https://robodk.com/doc/en/PlugIns/index.html).

Documentation
---------------

Each package implements the following modules/classes:

 * The [robolink](https://robodk.com/doc/en/PythonAPI/robodk.html#robolink-py) module is the link to RoboDK.
 * The [Item](https://robodk.com/doc/en/PythonAPI/robodk.html#robodk.robolink.Item) module: any item from the RoboDK item tree can be retrieved. Items are represented by the object Item. An item can be a robot, a reference frame, a tool, an object or a specific project.
 * The [robodk](https://robodk.com/doc/en/PythonAPI/robodk.html) module includes a robotics toolbox for pose operations. This toolbox is inspired from [Peter Corke's Robotics Toolbox](https://petercorke.com/toolboxes/robotics-toolbox/).


You can find more information about RoboDK API in our documentation.
 * [Introduction to the RoboDK API](https://robodk.com/doc/en/RoboDK-API.html#PythonAPI)
 * [Introduction to RoboDK for robot simulation and offline programming](https://robodk.com/offline-programming)
 * [The `robodk` package for Python](https://robodk.com/doc/en/PythonAPI/index.html)
 * [C++ version of the API](https://robodk.com/doc/en/CppAPI/index.html)
 * [C# version of the API (NuGet)](https://robodk.com/doc/en/CsAPI/index.html)
 * [PlugIn interface (C++)](https://robodk.com/doc/en/PlugIns/index.html)

Requirements
------------
* [RoboDK Simulation Software](https://robodk.com/download)

The RoboDK API can be used with a free RoboDK license.

Example
------------

The following script shows an example that uses the `robodk` package for robot simulation and offline programming. For more examples using the API, see our [documented examples](https://robodk.com/doc/en/PythonAPI/examples.html).

```python
from robodk.robolink import *      # RoboDK's API
from robodk.robomath import *      # Math toolbox for robots

# Start the RoboDK API:
RDK = Robolink()

# Get the robot item by name:
robot = RDK.Item('Fanuc LR Mate 200iD', ITEM_TYPE_ROBOT)

# Get the reference target by name:
target = RDK.Item('Target 1')
target_pose = target.Pose()
xyz_ref = target_pose.Pos()

# Move the robot to the reference point:
robot.MoveJ(target)

# Draw a hexagon around the reference target:
for i in range(7):
    ang = i*2*pi/6 #ang = 0, 60, 120, ..., 360

    # Calculate the new position around the reference:
    x = xyz_ref[0] + R*cos(ang) # new X coordinate
    y = xyz_ref[1] + R*sin(ang) # new Y coordinate
    z = xyz_ref[2]              # new Z coordinate
    target_pos.setPos([x,y,z])

    # Move to the new target:
    robot.MoveL(target_pos)

# Trigger a program call at the end of the movement
robot.RunCode('Program_Done')

# Move back to the reference target:
robot.MoveL(target)
```

Post Processors
------------------

The same script used for simulation can be used for robot programming offline. This means a program will be automatically generated for your robot controller to reproduce the movements on the robot.
RoboDK supports a large number of robot controllers and it is easy to include compatibility for new robot controllers using Post Processors.

More information about robot post processors here:

 * [Quick introduction to RoboDK post processors](https://robodk.com/help#PostProcessor)
 * [How to use Post Processors](https://robodk.com/doc/en/Post-Processors.html)
 * [Technical Reference](https://robodk.com/doc/en/PythonAPI/postprocessor.html)


You can find the most up to date list of supported robot controllers in our documentation for [Post processors](https://robodk.com/doc/en/Post-Processors.html#AvailablePosts).

<details>
<summary>Preview of supported robot controllers</summary>

* ABB RAPID IRC5: for ABB IRC5 robot controllers
* ABB RAPID S4C: for ABB S4C robot controllers
* Adept Vplus: for Adept V+ programming language
* Allen Bradley Logix5000: for Allen Bradley Logix5000 PLC
* Aubo: for AUBO robot controllers
* CLOOS: for CLOOS robot controllers
* Comau C5G: for Comau C5G robot controllers
* Denso PAC: for Denso RC7 (and older) robot controllers (PAC programming language)
* Denso RC8: for Denso RC8 (and newer) robot controllers (PacScript programming language)
* Dobot: for educational Dobot robots
* Doosan: for Doosan collaborative robots
* Epson: for Epson robot controllers
* Fanuc R30iA: for Fanuc R30iA and R30iB robot controllers
* Fanuc R30iA_Arc: for Fanuc Arc welding
* Fanuc RJ3: for Fanuc RJ3 robot controllers
* GCode BnR: for B&R robot controllers
* GSK: for GSK robots
* HCR: for Hanwha robot controllers
* HIWIN HRSS: for HIWIN robots
* Hyundai: for Hyundai robot controllers
* KAIRO: for Keba Kairo robot controllers
* Kinova: for Kinova robots
* Kawasaki: for Kawasaki AS robot controllers
* KUKA IIWA: for KUKA IIWA sunrise programming in Java
* KUKA KRC2: for KUKA KRC2 robot controllers
* KUKA KRC2_CamRob: for KUKA CamRob milling option
* KUKA KRC2_DAT: for KUKA KRC2 robot controllers including DAT data files
* KUKA KRC4: for KUKA KRC4 robot controllers
* KUKA KRC4_Config: for KUKA KRC4 robot controllers with configuration data in each line
* KUKA KRC4_DAT: for KUKA KRC4 robot controllers including DAT data files
* Mecademic: for Mecademic's script code required by the Meca500 robot
* Mecademic Python: it generates a Python script that can control the Mecademic Meca500 robot remotely.
* Mitsubishi: for Mitsubishi robot controllers
* Motoman/Yaskawa: for different Motoman robot controllers using Inform II and Inform III (JBI)
* Nachi AX FD: for Nachi AX and FD robot controllers
* Omron: for Omron/Techman robot controllers
* OTC: for Daihen OTC robot controllers
* Panasonic: For Panasonic PRG programs (requires Panasonic G2PC tools to compile ASCII files to binary files)
* Precise: for Precise Scara robots
* Robostar: for Robostar robot controllers
* Siasun: for Siasun robot controllers
* Siemens_Sinumerik: for Siemens Sinumerik ROBX robot controller
* Staubli VAL3: to generate Staubli VAL3 robot programs (CS8 controllers and later). It inlines the robot movements.
* Staubli VAL3_Machining: for Staubli VAL3 controllers that have the Machining HSM option.
* Staubli S6: for Staubli S6 robot controllers
* Toshiba: for Toshiba robots
* Techman: for Omron/Techman robot controllers
* Universal Robots: for UR robots, it generates linear movements as pose targets
* Universal Robots URP: for UR robots, it generates a URP that can be loaded and modified in Polyscope (the UR robot controller)
* Universal Robots_RobotiQ: for UR robots including support for RobotiQ gripper
* Universal Robots_MoveP: for UR robots, it generates linear movements as MoveP commands
* Yamaha: for Yamaha robots
</details>

More about RoboDK
----------------

* [Main website](https://robodk.com/)
* [RoboDK Documentation](https://robodk.com/doc/en/Basic-Guide.html)
* [Blog](https://robodk.com/blog)
