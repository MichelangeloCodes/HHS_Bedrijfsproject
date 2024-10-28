
# Use Ubuntu Jammy as the base image
FROM ubuntu:22.04

#######################
# Install ROS2 Humble #
#######################

# Set non-interactive environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Update packages, install locales, and set the locale
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales software-properties-common curl && \
    locale-gen en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

RUN apt-get install -y git

# Set the LANG environment variable
ENV LANG=en_US.UTF-8

# Add ROS 2 repository and install ROS 2, rosdep, and git
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && \
    apt-get install -y ros-humble-desktop python3-rosdep

# Initialize rosdep
RUN rosdep init && \
    rosdep update

# Source ROS 2 in .bashrc
#RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

#######################
# Start with micro-ROS #
#######################

# Create a workspace and download the micro-ROS tools
RUN mkdir ~/microros_ws && \
    cd ~/microros_ws && \
    git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup && \
    rosdep install --from-paths src --ignore-src -y
    #colcon build

#################################
# Clean up unnecessary packages #
#################################

RUN apt-get remove --purge -y locales software-properties-common curl python3-pip git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

