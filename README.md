# Mobile Robotics (CE/EE 468) — Samee

ROS 2 workspace for CE/EE 468 Mobile Robotics, Fall 2026.

| Folder | What it is |
|---|---|
| [`hw1_problem2/`](hw1_problem2/) | **HW1 Problem 2 — Getting to know ROS** (individual work): install evidence, videos, commands, setup log |
| [`src/char_talk/`](src/char_talk/) | ROS 2 package for Problem 2(c): char publisher + subscriber |
| [`src/turtle_wave/`](src/turtle_wave/) | ROS 2 package for Problem 2(f): cosine-wave turtle |

**Environment:** Windows → WSL2 → Ubuntu 24.04 → ROS 2 Jazzy Jalisco + Gazebo Harmonic (Gazebo Sim 8.15.0)

## Build

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```
