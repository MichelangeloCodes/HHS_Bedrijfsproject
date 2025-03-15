// CoreXY Control System for Arduino  
  // This program receives target coordinates via serial communication,  
  // processes movement commands, and controls two stepper motors using the AccelStepper library.  
  // Designed for integration with a Raspberry Pi (TurtleBot) and only functions correctly  
  // if the TurtleBot is properly programmed.  

  // Written by Team PioneerBot for the Smart Sensor Systems research group  
  // at The Hague University of Applied Sciences.  

// First include the AccelStepper.h library
#include <AccelStepper.h>

// Definitions and global variables
  #define degtorad 0.0174532925
  #define radtodeg 57.2957795

  // Motor pin definitions:
  #define motor1Pin1  2      // IN1 on the ULN2003 driver
  #define motor1Pin2  3      // IN2 on the ULN2003 driver
  #define motor1Pin3  4     // IN3 on the ULN2003 driver
  #define motor1Pin4  5     // IN4 on the ULN2003 driver

  // Motor pin definitions:
  #define motor2Pin1  6      // IN1 on the ULN2003 driver
  #define motor2Pin2  7      // IN2 on the ULN2003 driver
  #define motor2Pin3  8     // IN3 on the ULN2003 driver
  #define motor2Pin4  9     // IN4 on the ULN2003 driver

  // Define the AccelStepper interface type: 4 wire motor in half step mode:
  #define MotorInterfaceType 8

  // Steps per revolution for 28BYJ-48 in half-step mode:
  #define STEPS_PER_REV 4076

  // Distance of movement of belt per revolution of pulley
  #define DIST_PER_REV 40.0 // [mm]

  // Steps of 28BYJ-48 per mm of belt movement
  #define STEPS_PER_MM 102 // [steps]

  // Motor 1 
  AccelStepper motor1(MotorInterfaceType, motor1Pin1, motor1Pin3, motor1Pin2, motor1Pin4);

  // Motor 2
  AccelStepper motor2(MotorInterfaceType, motor2Pin1, motor2Pin3, motor2Pin2, motor2Pin4);


// Setup function for the arduino
  // Sets up the serial connection with the RPi (turtlebot) and the motors
void setup() {
  Serial.begin(9600);

  Serial.println("TEST SERIAL");
  delay(1000); // 1 seconde wachten

  // Set the maximum speed and acceleration for both motors
  motor1.setAcceleration(500);  // [steps/s^2]
  motor1.setMaxSpeed(1000);  // [steps/s]

  motor2.setAcceleration(500);  
  motor2.setMaxSpeed(1000);

}


// Loop function
  // Waits for serial data, parses coordinates, and controls the CoreXY system.  
void loop() {
  // Wait to receive serial data from RPi (turtlebot)
  if (Serial.available() > 0) {
    String receivedData = Serial.readStringUntil('\n');  // Read the full line until newline
    receivedData.trim();  // Remove unnecessary whitespace

    // Variables to store the parsed values
    float delta_x, delta_y, delta_w;
    
    // CSV parsing: Expected format "x,y,w"
    int firstComma = receivedData.indexOf(',');
    int secondComma = receivedData.lastIndexOf(',');

    if (firstComma > 0 && secondComma > firstComma) {
        delta_x = receivedData.substring(0, firstComma).toFloat();
        delta_y = receivedData.substring(firstComma + 1, secondComma).toFloat();
        delta_w = receivedData.substring(secondComma + 1).toFloat();

        // Run Go To Setpoint function with the received data
        goto_sp(delta_x, delta_y, delta_w);

        // Send success message to RPi (turtlebot)
        Serial.println(1);

    } else {
        // Send error message to RPi (turtlebot)
        Serial.println("Error: Incorrect CSV format received!");
    }
  }
}


// Go To setpoint function
  // This function takes a x and y position and a rotation and 
  // calculates to where the CoreXY platform must move. The 
  // function then controls the motors so that they move the 
  // CoreXY platform to the correct position.
void goto_sp(float x, float y, float w){
  // Compensate for angular rotation
  float move_x = x * cos(w*degtorad);
  float move_y = y * cos(w*degtorad);

  long sp_motor1 = ((move_x + move_x)*STEPS_PER_MM);
  long sp_motor2 = ((move_x - move_y)*STEPS_PER_MM);

  // Control the motors
  motor1.moveTo(sp_motor1);
  motor2.moveTo(sp_motor2);

  // Wait to continue
  run_till_done();
}


// Zero function
  // Moves the platform to the zero position
void zero(){
  // Set 0 as setpoint
  motor1.moveTo(0);
  motor2.moveTo(0);

  // Wait to continue
  run_till_done();
}


// Run till done function
  // This function ensures that the code does not continue but 
  // remains "stuck" until the motors are in the correct position.
void run_till_done(){
  // Run the motors to their target position
  while (motor1.distanceToGo() != 0 && motor2.distanceToGo() != 0) {
    if (motor1.distanceToGo() != 0) {
      motor1.run();
    } else {
      motor1.disableOutputs();
    }
    if (motor2.distanceToGo() != 0) {
      motor2.run();
    } else {
      motor2.disableOutputs();
    }
  } 
}