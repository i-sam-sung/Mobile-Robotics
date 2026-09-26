# (g) Setup log

Every obstacle during setup, with the raw error text left as it appeared. Screenshots are in [`evidence/`](evidence/).

> Minutes for errors 2–4 are estimated from the timestamps of my screenshots (first error screenshot → first working screenshot); error 1 is my own estimate.

| # | Exact error text (short) | What I tried | What fixed it | Minutes lost | TA involved? |
|---|---|---|---|---|---|
| 1 | `Windows Subsystem for Linux has no installed distributions.` | Searched Start menu for Ubuntu; `wsl -l -v` | Re-ran `wsl --install -d Ubuntu-24.04`; the first run had only installed the WSL platform, not Ubuntu | 30 | No |
| 2 | `gz: command not found` | `dpkg -l \| grep ros-jazzy-ros-gz` (all installed); launching via `ros2 launch ros_gz_sim …` (gave error 2b); `which gz` | `source /opt/ros/jazzy/setup.bash` — the terminal had loaded ROS before Gazebo was installed | ≈ 10 | No |
| 3 | `SyntaxError: '(' was never closed` (colcon build of `char_talk`) | Read the traceback; the relevant line was `setup.py` line 5 | Rewrote `setup.py` cleanly; a bracket had been lost while editing `entry_points` in nano | ≈ 10–20 | No |
| 4 | `fatal: not a git repository`, then `fatal: empty ident name … not allowed` / `error: src refspec main does not match any`, then HTTPS push asking for a password | `git init`; `git config --global user.name/email`; Personal Access Token; Windows Git Credential Manager (not installed) | Installed GitHub CLI: `gh auth login` (browser device login) + `gh auth setup-git`, then `git push` | ≈ 35 | No |

---

## Error 1 — Ubuntu missing after WSL install + restart

**Exact error text** (`wsl -l -v` in PowerShell):
```
Windows Subsystem for Linux has no installed distributions.
You can resolve this by installing a distribution with the instructions below:

Use 'wsl.exe --list --online' to list available distributions
and 'wsl.exe --install <Distro>' to install.
```
**Context:** Ran `wsl --install -d Ubuntu-24.04` in admin PowerShell and restarted. Ubuntu did not open and was not in the Start menu.
**Fix:** Ran `wsl --install -d Ubuntu-24.04` again. The first run only installed the WSL platform; the second downloaded and installed Ubuntu 24.04.

---

## ROS 2 Jazzy install — no errors
Locale setup, `universe` repository, `ros2-apt-source`, `ros-jazzy-desktop` + `ros-dev-tools`, and sourcing in `~/.bashrc` all ran without errors.

---

## Error 2 — `gz` command not found

**Exact error text:**
```
samee@Samee:~$ gz sim shapes.sdf
gz: command not found
```
Screenshot: [`evidence/err2_gz_command_not_found.png`](evidence/err2_gz_command_not_found.png)

**What I tried:**
1. `dpkg -l | grep ros-jazzy-ros-gz` → all six `ros-gz` packages show `ii` (installed, v1.0.24-1noble). [`evidence/err2_dpkg_ros_gz_installed.png`](evidence/err2_dpkg_ros_gz_installed.png)
2. Launching through ROS instead gave a second error (2b below). [`evidence/err2b_launch_nonetype_lower.png`](evidence/err2b_launch_nonetype_lower.png)
3. `source /opt/ros/jazzy/setup.bash` then `which gz` → `/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz`. `dpkg -l | grep vendor | grep gz` shows all Gazebo vendor packages installed (gz-sim-vendor = Gazebo Sim 8.15.0, i.e. Harmonic). [`evidence/err2_which_gz_and_vendor_packages.png`](evidence/err2_which_gz_and_vendor_packages.png)

**Root cause:** On Jazzy, the `gz` program lives inside ROS's own folder (`/opt/ros/jazzy/opt/gz_tools_vendor/bin/`) and is only added to `PATH` when `/opt/ros/jazzy/setup.bash` is sourced. My terminal had sourced ROS *before* Gazebo was installed.
**Fix:** `source /opt/ros/jazzy/setup.bash` (or open a new terminal). `gz sim shapes.sdf` then opened normally; no graphics workaround was needed.

### Error 2b — launch file exception (side effect, not pursued)
```
samee@Samee:~$ ros2 launch ros_gz_sim gz_sim.launch.py gz_args:=shapes.sdf
[INFO] [launch]: All log files can be found below /home/samee/.ros/log/2026-09-25-01-09-13-811568-Samee-20283
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): 'NoneType' object has no attribute 'lower'
```
Happened in the same un-refreshed terminal while trying an alternative route. Not needed once `gz` was found; not re-tested.

---

## Error 3 — colcon build failed: SyntaxError in setup.py

**Exact error text** (key lines; full output in [`evidence/err3_colcon_syntaxerror_1.png`](evidence/err3_colcon_syntaxerror_1.png), [`evidence/err3_colcon_syntaxerror_2.png`](evidence/err3_colcon_syntaxerror_2.png)):
```
Starting >>> char_talk
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3/dist-packages/setuptools/_distutils/core.py", line 267, in run_setup
    exec(code, g)
  File "<string>", line 5
    setup(
         ^
SyntaxError: '(' was never closed
...
Failed   <<< char_talk [0.31s, exited with code 1]

Summary: 0 packages finished [0.67s]
  1 package failed: char_talk
  1 package had stderr output: char_talk
```
**Context:** After editing the `entry_points` block of `src/char_talk/setup.py` in nano.
**Fix:** A bracket was lost during the edit. Replaced `setup.py` with a clean version; rebuild → `1 package finished`.

---

## Error 4 — git commit / push to GitHub

**Exact error text:**
```
fatal: not a git repository (or any of the parent directories): .git
```
[`evidence/err4_not_a_git_repository.png`](evidence/err4_not_a_git_repository.png)
```
Author identity unknown

*** Please tell me who you are.
...
fatal: empty ident name (for <samee@Samee.localdomain>) not allowed
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/i-sam-sung/Mobile-Robotics.git'
```
[`evidence/err4_author_identity_unknown.png`](evidence/err4_author_identity_unknown.png)
```
ls: cannot access '/mnt/c/Program Files/Git/mingw64/bin/': No such file or directory
```
[`evidence/err4_no_git_for_windows.png`](evidence/err4_no_git_for_windows.png)

**What I tried:** `git init` (had been skipped); set `user.name` / `user.email`; a Personal Access Token as the HTTPS password (did not work for me); reusing Windows' Git Credential Manager from WSL (Git for Windows not installed).
**Fix:** `sudo apt install -y gh`, `gh auth login` (GitHub.com → HTTPS → web browser login with the one-time code from the terminal at github.com/login/device), `gh auth setup-git`, then `git push -u origin main`. [`evidence/err4_github_device_login.png`](evidence/err4_github_device_login.png)
**Why it differed from my other courses:** Ubuntu in WSL has its own separate git with no login helper; the automatic browser login I was used to comes from git tools on Windows.

---

_AI use: Used Claude to diagnose installation and build errors (permitted infrastructure use)._
