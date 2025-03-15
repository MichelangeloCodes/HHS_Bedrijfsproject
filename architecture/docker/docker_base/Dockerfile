# Use the official Ubuntu Jammy image as the base
FROM ros:humble-ros-base-jammy

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8


#################
# UPDATE SYSTEM #
#################

# Update package lists, enable the universe repository, and install necessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get install -y python3 python3-pip git python3-colcon-common-extensions 


#############
# MICRO-ROS #
#############

RUN source /opt/ros/$ROS_DISTRO/setup.bash && \
    mkdir -p ~/microros_ws/src && \
    cd ~/microros_ws/src && \
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git && \
    cd ~/microros_ws && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y && \
    colcon build && \
    source install/local_setup.bash && \
    ros2 run micro_ros_setup create_firmware_ws.sh freertos esp32

##############################
# INSTALL TURTLEBOT4 PACKAGES #
##############################

RUN apt-get install -y turtlebot4  

######################
# CLEAN UP CONTAINER #
######################

# Clean up to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Specify entrypoint or command if needed
# CMD ["your-command-here"]

