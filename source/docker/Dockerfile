# INSTALL UBUNTU JAMMY AS BASE :: https://hub.docker.com/_/ubuntu
FROM ubuntu:22.04

# UPDATE UBUNTU PACKAGES
RUN sudo apt update -y && sudo apt upgrade -y

# INSTALL ROS2 HUMBLE :: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
RUN locale  

RUN sudo apt update && sudo apt install locales
RUN sudo locale-gen en_US en_US.UTF-8
RUN sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8

RUN locale  

RUN sudo apt install software-properties-common
RUN sudo add-apt-repository universe

RUN sudo apt update && sudo apt install curl -y
RUN sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN sudo apt update
RUN sudo apt upgrade

RUN sudo apt install ros-humble-desktop

RUN source /opt/ros/humble/setup.bash

# REMOVE GIT
# ...

# MAKE WORK DIRECTORY