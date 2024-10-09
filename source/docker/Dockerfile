# INSTALL UBUNTU JAMMY AS BASE :: https://hub.docker.com/_/ubuntu
FROM ubuntu:22.04

# UPDATE UBUNTU PACKAGES
RUN apt update -y && apt upgrade -y

# INSTALL ROS2 HUMBLE :: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
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

# REMOVE GIT
# ...

# MAKE WORK DIRECTORY