# when building use the following commands to convert it to arm64 for the raspberry pi

# docker buildx create --use
# docker buildx build --platform linux/arm64 -t your-image-name .

# OR

# docker buildx build --platform linux/amd64,linux/arm64 -t your-image-name --push .

# both commands not tested


# Use the official Ubuntu Jammy image as the base
FROM ros:humble-ros-base-jammy

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists, enable the universe repository, and install necessary packages
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    python3-colcon-common-extensions \
    build-essential \
    ros-$ROS_DISTRO-ros-base && \
    add-apt-repository universe && \
    apt-get update

# Create a workspace and clone the micro-ROS tools
RUN mkdir -p /home/microros_ws/src && \
    cd /home/microros_ws/src && \
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git

# Update dependencies using rosdep
RUN rosdep update && \
    rosdep install --from-paths /home/microros_ws/src --ignore-src -y

# Optionally, build micro-ROS tools if needed
# RUN cd /home/microros_ws && colcon build

# Set the entrypoint to source the ROS environment and start a shell
#CMD ["bash", "-c", "source /opt/ros/$ROS_DISTRO/setup.bash && exec bash"]

