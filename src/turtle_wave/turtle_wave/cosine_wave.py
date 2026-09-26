import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def wrap(a):
    """Keep an angle between -pi and pi."""
    return math.atan2(math.sin(a), math.cos(a))


class CosineWave(Node):
    def __init__(self):
        super().__init__('cosine_wave')
        self.A = self.declare_parameter('A', 2.0).value       # wave height
        self.k = self.declare_parameter('k', 1.0).value       # how tightly it wiggles
        self.c = self.declare_parameter('c', 1.0).value       # speed to the right
        self.length = self.declare_parameter('length', 10.0).value  # how far right to drive
        self.K_th = 4.0   # correction gain for heading error
        self.K_y = 2.0    # correction gain for being above/below the wave

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.start = None
        self.done = False
        self.get_logger().info(f'Cosine wave: A={self.A}, k={self.k}, c={self.c}')

    def on_pose(self, pose):
        if self.done:
            return
        if self.start is None:                       # first pose = top of the wave
            self.start = (pose.x, pose.y)
            self.get_logger().info(f'Starting at x={pose.x:.2f}, y={pose.y:.2f}')
        x0, y_top = self.start
        A, k, c = self.A, self.k, self.c

        msg = Twist()
        if pose.x - x0 < self.length:
            p = k * (pose.x - x0)                    # plays the role of k*c*t
            slope = -A * k * math.sin(p)             # dy/dx of the wave
            # feed-forward: the hand-derived v and omega
            v = c * math.sqrt(1 + slope ** 2)
            omega_ff = -A * k ** 2 * c * math.cos(p) / (1 + slope ** 2)
            # feedback: how far off are we?
            y_des = y_top - A + A * math.cos(p)      # where the wave is at this x
            e_y = pose.y - y_des                     # + means above the wave
            e_th = wrap(pose.theta - math.atan(slope))  # + means pointing too far left
            msg.linear.x = v
            msg.angular.z = omega_ff - self.K_th * e_th - self.K_y * e_y
        else:
            self.done = True
            self.get_logger().info('Done.')
        self.pub.publish(msg)                        # all zeros once done: turtle stops


def main(args=None):
    rclpy.init(args=args)
    node = CosineWave()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
