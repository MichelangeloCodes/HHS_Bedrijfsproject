import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import time
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String  # Voor de toestemming publisher
from irobot_create_msgs.action import Dock, Undock  # Dock en Undock acties

from .usb_arduino_connection import setup_serial, send_data, receive_ack


class PoseFollower(Node):
    def __init__(self):
        super().__init__('pose_follower')

        # Setup verbinding met Arduino
        self.ser = setup_serial()    

        # Actie clients voor navigatie, docking en undocking
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.dock_action_client = ActionClient(self, Dock, '/dock')
        self.undock_action_client = ActionClient(self, Undock, '/undock')

        # Wachten tot servers beschikbaar zijn
        self.get_logger().info("Waiting for the action servers to be available...")
        self._action_client.wait_for_server()
        self.dock_action_client.wait_for_server()
        self.undock_action_client.wait_for_server()
        self.get_logger().info("Action servers available!")

        # Publisher voor toestemmingssignaal naar `/toestemming_meten`
        self.toestemming_publisher = self.create_publisher(String, '/toestemming_meten', 10)

        # Variabelen voor tracking van snelheid en vorige positie
        self.last_pose = None
        self.still_time = 0  # Tijd in seconden dat de robot stil heeft gestaan
        self.still_threshold = 2.0  # Drempel in seconden om stilstand te detecteren

        # Doelen instellen
        self.target_poses = [
            #self.create_pose(-4.0, -1.0, 1.0),
            #self.create_pose(-2.0, -2.0, 1.0),
            #self.create_pose(-6.0, 1.5, 0.5),
            #self.create_pose(-0.3, -0.15, 1.0)
            self.create_pose(-3.0, -5.46, 1.0),
            self.create_pose(-3.9, -1.86, 1.0),
            self.create_pose(-7.44, -1.0, 1.0),
            self.create_pose(-2.16, -1.74, 1.0)
        ]
        self.current_target_index = 0

        # Variabelen voor huidige pose en tijd
        self.current_pose = None
        self.start_time = time.time()

        # Variabele voor toestemmingsstatus (start als None)
        self.toestemming_status = None
        self.sent_permission = False  # Toegevoegd om toestemming één keer per locatie te sturen

        # Abonnement op /amcl_pose
        self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

        # Abonnement voor het ontvangen van toestemming
        self.create_subscription(
            String,
            '/toestemming_meten',
            self.toestemming_callback,
            10
        )

        # Start navigatie naar eerste doel
        self.move_to_pose(self.target_poses[self.current_target_index])

        # Timer voor tracking
        self.timer = self.create_timer(1.0, self.track_pose)

    def create_pose(self, x, y, w):
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
        future = self._action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

        self.start_time = time.time()

    def goal_response_callback(self, future):
        result = future.result()
        if result:
            self.get_logger().info("Goal accepted, waiting for result...")

    def pose_callback(self, msg):
        self.current_pose = msg.pose.pose

    def track_pose(self):
        current_time = time.time()
        elapsed_time = round(current_time - self.start_time, 2)

        is_standing_still = False  # Boolean voor stilstandstatus

        if self.current_pose is not None:
            self.get_logger().info(
                f"[INFO] [Time: {elapsed_time:.1f} s - Target {self.current_target_index + 1} - "
                f"Pose X: {self.current_pose.position.x:.2f}, Y: {self.current_pose.position.y:.2f}]"
            )

            # Controleer of de robot stilstaat
            if self.last_pose:
                dx = self.current_pose.position.x - self.last_pose.position.x
                dy = self.current_pose.position.y - self.last_pose.position.y
                dz = self.current_pose.position.z - self.last_pose.position.z

                # Bereken de snelheid (afwijking van de positie)
                speed = (dx**2 + dy**2 + dz**2)**0.5

                # Als de snelheid lager is dan een drempel, beschouwen we de robot als stilstaand
                if speed < 0.05:  # Drempelwaarde voor snelheid (in meters)
                    self.still_time += 1  # Verhoog de stilstandtijd
                else:
                    self.still_time = 0  # Reset de stilstandtijd als er beweging is

                if self.still_time >= self.still_threshold:  # Als robot stil staat voor drempel tijd
                    self.get_logger().info("Robot is standing still for more than threshold time.")
                    is_standing_still = True  # Stel de boolean in dat de robot stilstaat
                else:
                    is_standing_still = False
            
            # Update de vorige pose voor de volgende tracking
            self.last_pose = self.current_pose

            # Conditie wanneer pose bereikt is of wanneer we 90 seconden gepasseerd zijn en de robot stil staat
            if ((self.is_pose_reached(self.target_poses[self.current_target_index], self.current_pose) or 
                    elapsed_time > 90) and is_standing_still):
                self.get_logger().info(f"Pose {self.current_target_index + 1} reached or timed out or robot is still.")

                if self.current_target_index < len(self.target_poses) - 1:
                    X_coor  = 0.0
                    Y_coor  = 0.0
                    W_orien = 0.0
                    send_data(self.ser, X_coor, Y_coor, W_orien)

                    if receive_ack(self.ser):
                        # Stuur toestemming naar /toestemming_meten als deze nog niet is verzonden
                        if not self.sent_permission:
                            self.send_toestemming_meten()
                            self.sent_permission = True  # Markeer dat toestemming is verzonden

                        # Wacht totdat toestemming "0" is ontvangen voordat verder gaat
                        if self.toestemming_status == "0":
                            if elapsed_time > 90:
                                time.sleep(2)

                            self.get_logger().info("Acknowledgment received, continuing to next pose...")
                            self.current_target_index += 1
                            self.move_to_pose(self.target_poses[self.current_target_index])
                            self.sent_permission = False

                    else:
                        self.get_logger().info("No valid acknowledgment, retrying...")
                else:
                    self.get_logger().info("Final pose reached. Initiating docking procedure...")
                    self.dock_robot()
        else:
            self.get_logger().info("Waiting for current pose to be received...")

    def is_pose_reached(self, target_pose, current_pose):
        margin_x = 0.30
        margin_y = 0.30
        margin_w = 0.20

        return (
            abs(current_pose.position.x    - target_pose.pose.position.x)    <= margin_x and
            abs(current_pose.position.y    - target_pose.pose.position.y)    <= margin_y and
            abs(current_pose.orientation.w - target_pose.pose.orientation.w) <= margin_w
        )

    def send_toestemming_meten(self):
        """Stuurt een 1 naar /toestemming_meten om metingen te starten."""
        msg = String()
        msg.data = "1"
        self.toestemming_publisher.publish(msg)
        self.get_logger().info("Toestemming voor metingen verzonden.")

    def dock_robot(self):
        self.get_logger().info("Docking the robot...")
        goal_msg = Dock.Goal()
        future = self.dock_action_client.send_goal_async(goal_msg)
        future.add_done_callback(self.dock_response_callback)

    def dock_response_callback(self, future):
        try:
            future.result()
            self.get_logger().info("Docking request completed successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to dock the robot: {str(e)}")

    def toestemming_callback(self, msg):
        """Callback voor toestemming_meten topic."""
        self.toestemming_status = msg.data
        self.get_logger().info(f"Toestemming status ontvangen: {self.toestemming_status}")


def main(args=None):
    rclpy.init(args=args)

    pose_follower = PoseFollower()

    rclpy.spin(pose_follower)

    pose_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
