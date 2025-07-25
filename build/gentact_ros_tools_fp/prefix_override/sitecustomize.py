import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/caleb/ros2_ws/src/gentact_ros_tools_fp/install/gentact_ros_tools_fp'
