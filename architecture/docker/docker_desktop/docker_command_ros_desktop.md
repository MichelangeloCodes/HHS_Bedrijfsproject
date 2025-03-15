# Docker commands

## start container in SHELL 1 
### to make use of GUI applications
```bash 
xhost +local:docker
```

### to start the container
```bash 
docker run -it --rm \
    --name ROS_DESKTOP \
    --privileged \
    --device /dev/ttyUSB0 \
    --device /dev/ttyUSB1 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network host \
    --mount type=bind,source="$HOME/Documents/pioneerbot/",target=/home/workspace \
    HHS/ros2_desktop:latest
```

## explained
-it                 :: the container starts interactive mode
--rm                :: removed after use, so if you want to change the container you have to change the image
                       with this tag you can experiment without consequences, because it will not be saved
--name              :: gives the container a name 
--privileged        :: grants the container access to USB ports and other devices
--mount             :: mounts a dir to the container, in this case the git repo gets mounted
--device            :: adds USB ports, container can utilise esp32 or for example a camera
-e                  :: grant acces to display if xhost permission is given
-v                  :: X11-unix display
image name          :: picks the image to run from with given tag [version]


## start container in SHELL X
if already a container is running, check for docker container id
```bash
docker ps
```
```bash
docker exec -it <container_id> /bin/bash
```
