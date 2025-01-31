from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, LogInfo
from launch_ros.actions import Node
import os

def generate_launch_description():
    # Forced path to the YAML file
    force_path = '/home/jerome/turtlebot4_ws/src/HHS_Bedrijfsproject/workspace/turtlebot4/turtlebot4_launch/turtlebot4_launch/mbrtc_lokaal.yaml'

    return LaunchDescription([
        # Log info for map localization
        LogInfo(
            msg="Info: Launching map localization..."
        ),

        # Start the map localization immediately (no timer)
        ExecuteProcess(
            cmd=[
                'ros2', 'launch', 'turtlebot4_navigation', 'localization.launch.py',
                f'map:={force_path}'  # Use forced path
            ],
            output='screen'
        ),
        
        # Log info for starting pose estimation after 10 seconds
        LogInfo(
            msg="Info: Starting pose estimation after 10 seconds..."
        ),

        # Start pose estimation after 10 seconds
        TimerAction(
            period=10.0,  # Delay for 10 seconds
            actions=[
                Node(
                    package='nav_pose_follower',
                    executable='pose_estimator',
                    name='pose_estimator',
                    output='screen'
                )
            ]
        ),
        
        # Log info for waiting 5 seconds after pose estimation before undocking
        LogInfo(
            msg="Info: Waiting 5 seconds after pose estimation before undocking..."
        ),

        # Wait 5 seconds after pose estimation, then undock the robot
        TimerAction(
            period=15.0,  # 10s from pose estimation + 5s wait
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'action', 'send_goal', '/undock', 'irobot_create_msgs/action/Undock', '{}'],
                    output='screen'
                )
            ]
        ),
        
        # Log info for NAV2
        LogInfo(
            msg="Info: Launching NAV2 after 30 seconds..."
        ),

        # Start NAV2 after 30 seconds
        TimerAction(
            period=30.0,  # Delay for 30 seconds
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'launch', 'turtlebot4_navigation', 'nav2.launch.py'],
                    output='screen'
                )
            ]
        ),
        
        # Log info for navigation pose follower
        LogInfo(
            msg="Info: Running navigation pose follower after 60 seconds..."
        ),

        # Run the navigation pose follower after 60 seconds
        TimerAction(
            period=60.0,  # Delay for 60 seconds
            actions=[
                Node(
                    package='nav_pose_follower',
                    executable='pose_follower',
                    name='pose_follower',
                    output='screen'
                )
            ]
        ),
    ])

