# Docker commands

## start container in SHELL 1 
### to make use of GUI applications
xhost +local:docker

### to start the container
docker run -it --rm \
    --name ROS_DESKTOP \
    --privileged \
    --mount type=bind,source="$HOME/Documents/HHS_Bedrijfsproject",target=/home/workspace \
    --device /dev/ttyUSB0 \
    --device /dev/ttyUSB1 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    HHS/ros2_desktop:latest


## explained
-it                 :: the container starts interactive mode
--rm                :: removed after use, so if you want to change the container you have to change the image
                       with this tag you can experiment without consequences, because it will not be saved
--name ROS_DESKTOP  :: gives the container a name 
--privileged        :: grants the container access to USB ports and other devices
--mount             :: mounts a dir to the container, in this case the git repo gets mounted
--device            :: adds USB ports, container can utilise esp32 or for example a camera
HHS/ros_base:latest :: picks the image to run from with given tag [version]


## start container in SHELL X
docker exec -it <container_name_or_id> /bin/bash

