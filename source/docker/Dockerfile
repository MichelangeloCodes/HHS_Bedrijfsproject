# INSTALL UBUNTU JAMMY AS BASE :: https://hub.docker.com/_/ubuntu
FROM ubuntu:22.04

# UPDATE UBUNTU PACKAGES
RUN apt update -y && apt upgrade -y

#######################
#   START WITH ROS    #
#######################

# https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

RUN locale  

RUN apt update && apt install locales -y
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8

RUN locale  

RUN apt install software-properties-common -y
RUN add-apt-repository universe

RUN apt update &&  apt install curl -y
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" |  tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update -y
RUN apt upgrade -y

RUN apt install ros-humble-desktop -y

RUN source /opt/ros/humble/setup.bash

#######################
# START WITH MICROROS #
#######################

# https://micro.ros.org/docs/tutorials/core/first_application_linux/

# Source the ROS 2 installation
RUN source /opt/ros/$ROS_DISTRO/setup.bash

# go to correct dir
RUN cd ~/

# Create a workspace and download the micro-ROS tools
RUN mkdir microros_ws && \
    cd microros_ws && \
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Update dependencies using rosdep
RUN apt update && rosdep update
RUN rosdep install --from-paths src --ignore-src -y

# Install pip
RUN apt-get install python3-pip

# Build micro-ROS tools and source them
RUN colcon build
RUN source install/local_setup.bash
