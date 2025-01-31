#!/bin/bash

# Undock the robot
ros2 action send_goal /undock irobot_create_msgs/action/Undock "{}"

# Start the map
ros2 launch turtlebot4_navigation localization.launch.py map:=mbrtc_lokaal.yaml

# Start NAV2
ros2 launch turtlebot4_navigation nav2.launch.py

# Run the navigation pose follower
ros2 run nav_pose_follower pose_follower
