"""Start new support nodes only. Sensors/SLAM/Nav2 are launched separately."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    config = PathJoinSubstitution([FindPackageShare('lidar_drone'), 'config', 'support.yaml'])
    use_sim = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        *[Node(package='lidar_drone', executable=name, name=name, output='screen',
               parameters=[config, {'use_sim_time': use_sim}])
          for name in ['odom_to_tf', 'goal_relay', 'laser_safety_stop', 'cmd_vel_mux']],
    ])
