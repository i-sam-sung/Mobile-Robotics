import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import Char


class CharSubscriber(Node):
    def __init__(self):
        super().__init__('char_subscriber')
        # subscribe: same type (Char) and SAME topic name as the publisher.
        # Every time a message arrives, ROS calls self.listener_callback
        self.subscription = self.create_subscription(
            Char, 'char_topic', self.listener_callback, 10)

    def listener_callback(self, msg):
        c = chr(msg.data)             # convert the number back to a letter, e.g. 97 -> 'a'
        self.get_logger().info(f'I heard: "{c}"')


def main(args=None):
    rclpy.init(args=args)
    node = CharSubscriber()
    try:
        rclpy.spin(node)              # keep running and waiting for messages
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
