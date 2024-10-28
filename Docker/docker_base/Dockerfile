# Use the official Ubuntu Jammy image as the base
FROM ros:humble-ros-base-jammy

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and enable the universe repository
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository universe && \
    apt-get update

# Create a workspace and clone the micro-ROS tools
RUN mkdir -p /home/microros_ws/src && \
    cd /home/microros_ws/src && \
    git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git

# Update dependencies using rosdep
RUN rosdep update && \
    rosdep install --from-paths /home/microros_ws/src --ignore-src -y

# Optionally, build micro-ROS tools
# RUN cd /home/microros_ws && colcon build

# Set the entrypoint to source the ROS environment and start a shell
#CMD ["bash", "-c", "source /opt/ros/$ROS_DISTRO/setup.bash && exec bash"]

