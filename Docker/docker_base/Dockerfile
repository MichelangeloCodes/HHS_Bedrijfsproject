FROM ros:humble-ros-base-jammy

# Source the ROS 2 installation
RUN source /opt/ros/$ROS_DISTRO/setup.bash

# Create a workspace and download the micro-ROS tools
RUN mkdir microros_ws
RUN cd microros_ws
RUN git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Update dependencies using rosdep
RUN apt-get update && rosdep update
RUN rosdep install --from-paths src --ignore-src -y

# Install pip
RUN command apt-get install python3-pip

# Build micro-ROS tools and source them
RUN colcon build
RUN source install/local_setup.bash