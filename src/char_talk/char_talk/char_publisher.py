import rclpy                          # the ROS 2 Python library
from rclpy.node import Node           # base class every ROS node is built from
from std_msgs.msg import Char         # the "char" message type the assignment asks for


class CharPublisher(Node):
    def __init__(self):
        super().__init__('char_publisher')             # the node's name inside ROS
        # create a publisher: message type Char, topic name 'char_topic', queue size 10
        self.publisher_ = self.create_publisher(Char, 'char_topic', 10)

    def publish_char(self, c):
        msg = Char()                  # make an empty Char message
        msg.data = ord(c)             # IMPORTANT: in ROS 2, Char stores a NUMBER (0-255),
                                      # so convert the letter to its code, e.g. 'a' -> 97
        self.publisher_.publish(msg)  # send it on the topic
        self.get_logger().info(f'Publishing: "{c}"')


def main(args=None):
    rclpy.init(args=args)             # start ROS for this program
    node = CharPublisher()
    try:
        while rclpy.ok():
            text = input('Enter a character: ')         # wait for keyboard input
            if len(text) != 1 or ord(text) > 255:
                print('Please type exactly one normal character.')
                continue
            node.publish_char(text)
    except (KeyboardInterrupt, EOFError):               # Ctrl+C / Ctrl+D stops cleanly
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

