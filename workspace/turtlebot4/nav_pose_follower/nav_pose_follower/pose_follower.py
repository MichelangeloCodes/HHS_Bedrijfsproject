import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from time import time
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_srvs.srv import Empty  # For docking service
from irobot_create_msgs.action import Dock, Undock  # Import the Dock and Undock actions

from .usb_arduino_connection import setup_serial, send_data, receive_ack


class PoseFollower(Node):
    def __init__(self):
        super().__init__('pose_follower')

        # setup connection to arudino - from usb_arduino_connection
        self.ser = setup_serial()    

        # Create an action client to send navigation goals
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Create action clients for docking and undocking
        self.dock_action_client = ActionClient(self, Dock, '/dock')
        self.undock_action_client = ActionClient(self, Undock, '/undock')

        # Wait for the action servers to be available
        self.get_logger().info("Waiting for the action servers to be available...")
        self._action_client.wait_for_server()
        self.dock_action_client.wait_for_server()
        self.undock_action_client.wait_for_server()
        self.get_logger().info("Action servers available!")

        # Define target poses
        self.target_poses = [
            self.create_pose(-4.0, -1.0, 1.0),  # Pose 1
            self.create_pose(-2.0, -2.0, 1.0),  # Pose 2
            self.create_pose(-6.0, 1.5, 0.5),   # Pose 3
            self.create_pose(-0.3, -0.15, 1.0)  # Pose 4
        ]
        self.current_target_index = 0  # Start with the first pose

        # Variable to store the current pose
        self.current_pose = None

        # Variable to track the start time
        self.start_time = time()

        # Subscriber to the robot's pose
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',  # Update with the correct topic
            self.pose_callback,
            10
        )

        # Start the navigation to the first target pose
        self.move_to_pose(self.target_poses[self.current_target_index])

        # Timer to periodically check the goal status and log the current pose
        self.timer = self.create_timer(1.0, self.track_pose)  # 1 second interval

    def create_pose(self, x, y, w):
        """Helper to create a PoseStamped object."""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = w
        return pose

    def move_to_pose(self, target_pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = target_pose

        self.get_logger().info(f"Sending goal to move to pose: {target_pose.pose.position.x}, {target_pose.pose.position.y}")

        # Send the goal and set up a callback for when the goal is done
        future = self._action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

        # Reset the timer whenever a new goal is sent
        self.start_time = time()

    def goal_response_callback(self, future):
        result = future.result()
        if result:
            self.get_logger().info("Goal accepted, waiting for result...")

    def pose_callback(self, msg):
        """Callback to update the current pose of the robot."""
        self.current_pose = msg.pose.pose

    def track_pose(self):
        """Track time and log current location/pose."""
        current_time = time()
        elapsed_time = round(current_time - self.start_time, 2)  # Round to 2 decimal places

        # Check if current_pose has been updated before proceeding
        if self.current_pose is not None:
            self.get_logger().info(
                f"[INFO] [Time: {elapsed_time:.1f} s - Target location: {self.current_target_index + 1} - "
                f"Pose X: {self.current_pose.position.x:.2f}, Y: {self.current_pose.position.y:.2f}]"
            )
            if self.is_pose_reached(self.target_poses[self.current_target_index], self.current_pose) or elapsed_time > 300:  # 300-second timeout
                self.get_logger().info(f"Pose {self.current_target_index + 1} reached or timed out after {elapsed_time} seconds.")
                
                #   DELTA MEEGEVEN AAN PLATFORM
                X_coor = 2.01
                Y_coor = -5.92
                W_orien = 1.00
                send_data(self, self.ser, X_coor, Y_coor, W_orien)

                if receive_ack(self, self.ser):
                    # Wait for acknowledgment before proceeding
                    if receive_ack(self.ser):
                        self.get_logger().info("Acknowledgment received, continuing...")

                        #   HIER AANGEVEN DAT WE KUNNEN METEN
                        #   WACHTEN TOT CONDITIE VAN METEN

                        #   ROBOT RIJDEN NAAR LOCATIE
                        self.current_target_index += 1
                        if self.current_target_index < len(self.target_poses):
                            self.move_to_pose(self.target_poses[self.current_target_index])
                        else:
                            self.get_logger().info("Final pose reached. Initiating docking procedure...")
                            self.dock_robot()  # Call docking procedure
                
                    else:
                        self.get_logger().info("No valid acknowledgment, retrying...")
                

        else:
            self.get_logger().info("Waiting for current pose to be received...")

    def is_pose_reached(self, target_pose, current_pose):
        """Check if the current pose is within a margin of the target pose."""
        margin_x = 0.15 * abs(target_pose.pose.position.x)  # 15% margin for x
        margin_y = 0.15 * abs(target_pose.pose.position.y)  # 15% margin for y
        margin_w = 0.25 * abs(target_pose.pose.orientation.w)  # 25% margin for w

        # Check if X, Y, and W are within the specified margins
        return (
            abs(current_pose.position.x - target_pose.pose.position.x) <= margin_x and
            abs(current_pose.position.y - target_pose.pose.position.y) <= margin_y and
            abs(current_pose.orientation.w - target_pose.pose.orientation.w) <= margin_w
        )

    def dock_robot(self):
        """Send a request to the docking service."""
        self.get_logger().info("Docking the robot...")
        goal_msg = Dock.Goal()  # Send the Dock action goal
        future = self.dock_action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.dock_response_callback)

    def dock_response_callback(self, future):
        """Handle the response from the docking service."""
        try:
            future.result()
            self.get_logger().info("Docking request completed successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to dock the robot: {str(e)}")


def main(args=None):
    rclpy.init(args=args)

    pose_follower = PoseFollower()

    rclpy.spin(pose_follower)

    pose_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

