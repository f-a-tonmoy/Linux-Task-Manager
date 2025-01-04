# Task Manager

## 📋 Overview
The **Task Manager** is a Python-based program designed to monitor and manage system processes on a Linux operating system. It provides detailed information about CPU usage, memory consumption, disk usage, and process hierarchy. Users can sort, filter, and explore processes, making it a lightweight alternative to GUI-based task managers.

---

## ✨ Features
1. **Process Monitoring**:
   - View all running processes with details such as CPU usage, memory consumption, disk usage, and thread count.
2. **Sorting**:
   - Sort processes by CPU, memory, disk usage, priority, or thread count (ascending or descending).
3. **Filtering**:
   - Filter processes by:
     - Type (system, user, or other).
     - Status (idle, sleeping, or running).
4. **Process Hierarchy**:
   - Display parent and child processes.
   - View threads of a specific process.
5. **Process Tree**:
   - Visualize the process tree using the `pstree` command.
6. **Update and Refresh**:
   - Update process information dynamically.

---

## 📂 Project Structure
```plaintext
├── tm.py                  # Main Python script for the task manager
├── README.md              # Project documentation
├── LICENSE                # Project license
```

---

## ⚙️ Requirements
- **Operating System**: Linux
- **Python Version**: 3.6 or higher
- **Dependencies**:
  - `psutil`: For process monitoring.
  - `platform`: To retrieve system information.
  - `distro`: To identify Linux distribution details.

Install the dependencies using:
```bash
pip install psutil distro
```

---

## 🚀 How to Use
1. **Run the Script**:
   ```bash
   python3 tm.py
   ```
2. **Available Commands**:
   - `all`: Display all processes.
   - `sorted [arg]`: Sort processes by CPU, memory, disk usage, etc.
     - Example: `sorted mem`, `sorted cpu ^`
   - `type [arg]`: Filter processes by type (e.g., `root`, `usr`).
     - Example: `type root sorted cpu`
   - `stat [arg]`: Filter processes by status (e.g., `idle`, `running`).
     - Example: `stat running sorted mem`
   - `parentof [pid]`: Display the parent of a specific process.
     - Example: `parentof 1234`
   - `childof [pid]`: Display children of a specific process.
     - Example: `childof 1234`
   - `threads [pid]`: Display threads of a specific process.
     - Example: `threads 1234`
   - `pstree`: Visualize the process tree.
   - `update`: Refresh process information.

3. **Exit the Program**:
   Use the `exit` or `terminate` command.

---

## 🌟 Limitations
- Platform-dependent: Works only on Linux.
- Lacks a GUI interface.
- Cannot terminate processes directly.
- Limited live updates for process data.

---

## 🛠️ Technologies Used
- **Programming Language**: Python
- **Modules**:
  - `psutil` for system and process monitoring.
  - `distro` and `platform` for system information retrieval.

---

## 📄 License
This project is licensed under the MIT License.

---

## 📬 Contact
For questions or feedback, please reach out via:
- **Fahim Ahamed (Tonmoy)**: [f.a.tonmoy00@gmail.com](mailto:f.a.tonmoy00@gmail.com)
