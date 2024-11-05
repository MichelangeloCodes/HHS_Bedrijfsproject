# Use Ubuntu Jammy as the base image
FROM ubuntu:22.04

# Set the shell to bash
SHELL ["/bin/bash", "-c"]

# Set non-interactive environment variable
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV ROS_DISTRO=humble


RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-opencv \
    bash-completion python3-argcomplete net-tools curl wget \
    software-properties-common git && \
    pip install --upgrade pip && \
    pip install argcomplete colcon-common-extensions && \
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


#######################
# Install ROS2 Humble #
#######################   
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    add-apt-repository universe && \
    apt-get update && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && \
    apt-get install -y ros-humble-desktop python3-rosdep && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


##############################
# Install TurtleBot packages #
##############################
RUN apt-get update && \
    apt-get install -y ros-humble-turtlebot4-desktop && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
    
#######################
# Start with micro-ROS #
#######################
RUN apt-get update && \
    mkdir -p /microros_ws/src && \
    cd /microros_ws && \
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup && \
    . /opt/ros/$ROS_DISTRO/setup.bash && \  
    rosdep init && \  
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y && \
    colcon build && \
    . install/local_setup.bash
