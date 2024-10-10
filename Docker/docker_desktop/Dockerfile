# Use Ubuntu Jammy as the base image
FROM ubuntu:22.04

# Set non-interactive environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Update packages, install locales, and set the locale
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales software-properties-common curl python3-pip && \
    locale-gen en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the LANG environment variable
ENV LANG=en_US.UTF-8

# Add ROS 2 repository and install ROS 2
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && \
    apt-get install -y ros-humble-desktop && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Source ROS 2 in .bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

#######################
# Start with micro-ROS #
#######################

# Create a workspace and download the micro-ROS tools
RUN mkdir -p /root/microros_ws/src && \
    cd /root/microros_ws/src && \
    git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git && \
    cd /root/microros_ws && \
    rosdep init && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y && \
    colcon build && \
    echo "source /root/microros_ws/install/local_setup.bash" >> /root/.bashrc

# Clean up unnecessary packages
RUN apt-get remove --purge -y locales software-properties-common curl python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

