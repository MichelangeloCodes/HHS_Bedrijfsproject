__/\\\\\\\\\\\\\__________________________________________________________________________________/\\\\\\\\\\\\\_______________________________        
 _\/\\\/////////\\\_______________________________________________________________________________\/\\\/////////\\\_____________________________       
  _\/\\\_______\/\\\__/\\\_________________________________________________________________________\/\\\_______\/\\\___________________/\\\______      
   _\/\\\\\\\\\\\\\/__\///______/\\\\\_____/\\/\\\\\\_______/\\\\\\\\______/\\\\\\\\___/\\/\\\\\\\__\/\\\\\\\\\\\\\\______/\\\\\_____/\\\\\\\\\\\_     
    _\/\\\/////////_____/\\\___/\\\///\\\__\/\\\////\\\____/\\\/////\\\___/\\\/////\\\_\/\\\/////\\\_\/\\\/////////\\\___/\\\///\\\__\////\\\////__    
     _\/\\\_____________\/\\\__/\\\__\//\\\_\/\\\__\//\\\__/\\\\\\\\\\\___/\\\\\\\\\\\__\/\\\___\///__\/\\\_______\/\\\__/\\\__\//\\\____\/\\\______   
      _\/\\\_____________\/\\\_\//\\\__/\\\__\/\\\___\/\\\_\//\\///////___\//\\///////___\/\\\_________\/\\\_______\/\\\_\//\\\__/\\\_____\/\\\_/\\__  
       _\/\\\_____________\/\\\__\///\\\\\/___\/\\\___\/\\\__\//\\\\\\\\\\__\//\\\\\\\\\\_\/\\\_________\/\\\\\\\\\\\\\/___\///\\\\\/______\//\\\\\___ 
        _\///______________\///_____\/////_____\///____\///____\//////////____\//////////__\///__________\/////////////_______\/////_________\/////____


Fase1: 2024-2025
Developers: Jerome Kemper, Mik van der Meer, Tym van Kuijk, Ties van der Sar en Matthijs Verburg.

## summary
Our goal is to design a mobile measurement robot that can autonomously drive in an indoor environment and perform environmental measurements. In this process we will be conducting research about the M5 stack and the TurtleBot 4. Using ROS2 we will develop a full programm for the Turtlebot 4. The M5 stack will collect al the data, and send it out using a still to be determined protocol. In this repository all programming will be developed and shared.


```markdown
# Setup Instructions

Follow these steps to set up the Pioneerbot environment.

## Clone the Repository

```bash
mkdir -p ~/Documents/Pioneerbot/src/
cd ~/Documents/Pioneerbot/src/
git clone [repository]
```

## Install Docker

Follow the instructions in the official Docker documentation:
- [Install Docker](https://docs.docker.com/engine/install/)
- [Execute Docker Post-Install Commands](https://docs.docker.com/engine/install/linux-postinstall/)

## Pull the Desktop Image
for now there are two tags: "ros2_desktop" and "ros2_arm"
replace <tag>
```bash
docker pull michelangelocodes/hhs:<tag>
```


Greetings
Team: Pioneerbot
