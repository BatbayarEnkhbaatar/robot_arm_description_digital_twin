from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from os import pathsep

def generate_launch_description():
        
    my_arm_robot_description = get_package_share_directory("my_arm_robot_description")
    my_arm_robot_description_prefix = get_package_prefix("my_arm_robot_description")
    model_path = os.path.join(my_arm_robot_description, "models")
    model_path += pathsep + os.path.join(my_arm_robot_description_prefix, "share")

    env_variable = SetEnvironmentVariable("GAZEBO_MODEL_PATH", model_path)


    model_arg = DeclareLaunchArgument(
            name="model", 
            default_value=os.path.join(get_package_share_directory("my_arm_robot_description"), "urdf", "model.urdf.xacro"),
            description="Absolute path to the robot URDF file"
        )

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration("model")]))

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )
    start_gazebo_server = IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py")))
    start_gazebo_client = IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(
        get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py")))
    
    spawn_robot = Node(
        package = "gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", "robot_arm_4DI_01", "-topic", "robot_description"],
        output ="screen"
    )
    return LaunchDescription([
        env_variable,
        model_arg,
        robot_state_publisher,
        start_gazebo_server,
        start_gazebo_client,
        spawn_robot
    ])