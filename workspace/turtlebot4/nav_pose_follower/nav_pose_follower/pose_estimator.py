import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import math

class PoseEstimator(Node):
    def __init__(self):
        super().__init__('pose_estimator')

        # Subscriber to /amcl_pose or /odom
        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',  # Modify this if your pose topic is different
            self.pose_callback,
            10
        )
        self.get_logger().info('Pose Estimator node has been started.')

    def pose_callback(self, msg):
        # Extract the position and orientation (quaternion)
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        # Convert quaternion to yaw (2D orientation)
        yaw = self.quaternion_to_yaw(orientation)

        # Log the 2D pose (position and yaw)
        self.get_logger().info(f'Robot position: x={position.x}, y={position.y}')
        self.get_logger().info(f'Robot yaw (orientation): {yaw:.2f} radians')

    def quaternion_to_yaw(self, orientation):
        # Convert quaternion to Euler angles (roll, pitch, yaw)
        siny = 2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy = 1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z)
        yaw = math.atan2(siny, cosy)
        return yaw

def main(args=None):
    rclpy.init(args=args)
    pose_estimator = PoseEstimator()
    rclpy.spin(pose_estimator)
    pose_estimator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

