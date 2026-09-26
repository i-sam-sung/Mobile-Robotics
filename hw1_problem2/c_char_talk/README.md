# (c) Char publisher and subscriber

Code: [`src/char_talk/char_talk/char_publisher.py`](../../src/char_talk/char_talk/char_publisher.py) and [`src/char_talk/char_talk/char_subscriber.py`](../../src/char_talk/char_talk/char_subscriber.py)

- **Publisher** (`char_publisher`) asks the user for one character, and publishes it on topic `char_topic` as `std_msgs/msg/Char`.
- **Subscriber** (`char_subscriber`) subscribes to `char_topic` and prints each character it receives.
- In ROS 2, `std_msgs/msg/Char` stores its value as a number (`uint8`), so the publisher sends `ord(c)` and the subscriber prints `chr(msg.data)`.
- Input longer than one character (e.g. `hello`) is rejected with a message.

## Run

```bash
cd ~/ros2_ws
colcon build --packages-select char_talk
source install/setup.bash

# terminal 1
ros2 run char_talk char_subscriber
# terminal 2
ros2 run char_talk char_publisher
```

## Video

[`publisher_subscriber_demo.mp4`](publisher_subscriber_demo.mp4): publisher on the left, subscriber on the right. Each character typed is printed by the subscriber; multi-character input is rejected.

_AI use: Used Claude for ROS boilerplate code and build steps._
