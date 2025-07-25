from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Generate URDF from xacro file (or read URDF file)
    urdf_file = PathJoinSubstitution([FindPackageShare('gentact_ros_tools_fp'), 'urdf', 'link5.xacro'])
    robot_description = ParameterValue(Command(['xacro ', urdf_file, ' namespace:=link5']), value_type=str)

    # Create nodes
    """
    Uncomment if using foxglove

    foxglove_bridge_node = Node(
        package='foxglove_bridge',
        executable='foxglove_bridge',
        name='foxglove_bridge',
        output='screen',
    )
    """

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description}]
    )

    static_transform_publisher_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'link5/base_link']
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2'
    )

    tof_listener = Node(
        package='udp_tof_listener',
        executable='udp_grid_listener_array',
        name='tof_listener'
    )

    pointcloud_talker = Node(
        package='pointcloud',
        executable='talker',
        name='tof_talker'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        #foxglove_bridge_node,
        TimerAction(period=1.0, actions=[robot_state_publisher_node]),  # 2 second delay
        TimerAction(period=2.0, actions=[static_transform_publisher_node]),  # 4 second delay
        TimerAction(period=3.0, actions=[tof_listener]),  # 4 second delay
        TimerAction(period=4.0, actions=[pointcloud_talker]),  # 4 second delay
        TimerAction(period=5.0, actions=[rviz_node]),  # 4 second delay
    ])