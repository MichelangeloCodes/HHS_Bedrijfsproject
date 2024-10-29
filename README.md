#  Pioneerbot
Fase1: 2024-2025
Developers: Jerome Kemper, Mik van der Meer, Tym van Kuijk, Ties van der Sar en Matthijs Verburg.

## summary

Our goal is to design a mobile measurement robot that can autonomously drive in an indoor environment and perform environmental measurements. In this process we will be conducting research about the M5 stack and the TurtleBot 4. Using ROS2 we will develop a full programm for the Turtlebot 4. The M5 stack will collect al the data, and send it out using a still to be determined protocol. In this repository all programming will be developed and shared.

# Setup Instructions

Follow these steps to set up the Pioneerbot environment.

## Clone the Repository

```bash
mkdir -p ~/Documents/Pioneerbot/src/
cd ~/Documents/Pioneerbot/src/
git clone git@github.com:MichelangeloCodes/HHS_Bedrijfsproject.git
```

## Install Docker

Follow the instructions in the official Docker documentation:
- [Install Docker](https://docs.docker.com/engine/install/)
- [Execute Docker Post-Install Commands](https://docs.docker.com/engine/install/linux-postinstall/)

## Pull the Desktop Image

for now there are two tags: "ros2_desktop" and "ros2_arm"
[dockerhub images] (https://hub.docker.com/repository/docker/michelangelocodes/hhs/tags)

replace <tag> with needed project version
```bash
docker pull michelangelocodes/hhs:<tag>
```
### start container
```bash
docker run -it --rm \
    --name ROS_DESKTOP \
    --mount type=bind,source="$HOME/Documents/Pioneerbot/",target=/home/workspace \
    --privileged \
    --device /dev/ttyUSB0 \
    --device /dev/ttyUSB1 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    michelangelocodes/hhs:ros2_desktop
```
command above works for desktop, else change last line 
more information in architecture/docker/docker_command_ros_desktop.md


Greetings
Team: Pioneerbot
