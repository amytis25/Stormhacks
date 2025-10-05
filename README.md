# 🎮 Log Roller Game - Arduino Edition

A 3D obstacle avoidance game built with Python, OpenGL, and Arduino controls. Navigate through lanes while dodging obstacles using joystick controls and ultrasonic sensor movements!

## 🎯 Game Overview

**Log Roller** is an immersive 3D game where players control a cube navigating through three lanes while avoiding moving obstacles. The game features both traditional keyboard controls and innovative Arduino hardware controls for a unique gaming experience.

### 🎬 Core Gameplay
- **Lane Navigation**: Move between left, center, and right lanes
- **Vertical Movement**: Duck under or jump over obstacles
- **Obstacle Avoidance**: Avoid spheres and wall obstacles
- **Survival Timer**: Track how long you survive
- **Progressive Difficulty**: Obstacles move faster over time

## 🕹️ Control Options

### 🎮 Keyboard Controls (`base.py`)
- **LEFT/A**: Move to left lane
- **RIGHT/D**: Move to right lane  
- **UP/W**: Jump over obstacles
- **DOWN/S**: Crouch under obstacles
- **R**: Reset timer
- **P**: Pause/resume timer

### 🔌 Arduino Controls (`base_arduino.py`)
- **Joystick X-axis**: Switch between lanes (left/center/right)
- **Ultrasonic Sensor**: Control height (close = crouch, far = jump)
- **Real-time positioning**: Smooth continuous movement based on distance

## 🛠️ Hardware Setup (Arduino)

### 📋 Required Components
- **Arduino Uno/Nano**
- **Analog Joystick Module**
- **HC-SR04 Ultrasonic Sensor**
- **Jumper wires**
- **Breadboard**

### 🔌 Wiring Diagram
```
Ultrasonic Sensor (HC-SR04):
- VCC → 5V
- GND → GND
- Trig → Pin 9
- Echo → Pin 10

Analog Joystick:
- VCC → 5V
- GND → GND
- VRx → A2 (X-axis)
- VRy → A3 (Y-axis)  
- SW → A4 (Button)
```

### 📤 Arduino Code
Upload `game_controller_combined.ino` to your Arduino:
- Reads both joystick and ultrasonic sensor
- Sends formatted data to Python game
- 115200 baud rate communication

## 💻 Software Requirements

### 🐍 Python Dependencies
```bash
pip install pygame PyOpenGL PyOpenGL-accelerate pyserial pillow numpy
```

### 📦 Required Files
- **Core Game**: `base.py` (keyboard) or `base_arduino.py` (Arduino)
- **Controls**: `controls.py`, `arduino_controls.py`
- **Graphics**: `shapes.py`, `lane_markers.py`, `game_timer.py`
- **Game Logic**: `sphere_manager.py`, `start_screen.py`, `button.py`
- **Assets**: `electric.png`, `background.png`

## 🚀 Getting Started

### 1️⃣ Keyboard Version
```bash
python base.py
```

### 2️⃣ Arduino Version
```bash
# Auto-detect (tries Arduino, falls back to keyboard)
python base_arduino.py

# Force Arduino mode
python base_arduino.py 1

# Force keyboard mode  
python base_arduino.py 2
```

### 3️⃣ First Time Setup
1. **Install dependencies** listed above
2. **Connect Arduino** (if using hardware controls)
3. **Upload Arduino sketch** (`game_controller_combined.ino`)
4. **Run the game** and enjoy!

## 🎨 Features

### 🌟 Visual Elements
- **3D OpenGL Graphics**: Smooth 60fps rendering
- **Textured Spheres**: Electric-themed obstacle textures
- **Lane Markers**: Visual guides for navigation
- **Background Textures**: Immersive environment
- **On-screen Timer**: Real-time survival tracking (MM:SS:mmm)

### 🎯 Game Mechanics
- **Collision Detection**: Precise 3D collision system
- **Lane-based Movement**: Three distinct travel lanes
- **Height-based Avoidance**: Jump/crouch mechanics
- **Progressive Spawning**: Dynamic obstacle generation
- **Game Over System**: Restart functionality with score display

### 🔧 Arduino Integration
- **Dual Control System**: Hardware + software controls
- **Real-time Sensor Data**: Live ultrasonic distance mapping
- **Smooth Movement**: Continuous position interpolation
- **Fallback System**: Automatic keyboard backup
- **Debug Monitoring**: Live sensor status display

## 🏗️ Architecture

### 📁 File Structure
```
Stormhacks/
├── base.py                     # Main game (keyboard)
├── base_arduino.py             # Main game (Arduino)
├── controls.py                 # Keyboard control system
├── arduino_controls.py         # Arduino control system
├── shapes.py                   # 3D object rendering
├── sphere_manager.py           # Obstacle management
├── lane_markers.py             # Visual lane guides
├── game_timer.py               # HUD timer display
├── start_screen.py             # Menu system
├── button.py                   # UI button component
├── game_controller_combined.ino # Arduino firmware
├── assets/
│   ├── electric.png            # Sphere texture
│   └── background.png          # Environment texture
└── README.md                   # This file
```

### 🔄 Game Flow
1. **Start Screen** → Player chooses to begin
2. **Game Setup** → Initialize OpenGL, controls, objects
3. **Main Loop** → Handle input, update physics, render
4. **Collision Check** → Detect obstacle hits
5. **Game Over** → Show final time, return to start

## 🎛️ Configuration

### ⚙️ Arduino Settings
- **Port**: Default COM3 (Windows) - modify in code if needed
- **Baud Rate**: 115200
- **Sensor Ranges**: 5-50cm for ultrasonic positioning
- **Joystick Threshold**: Adjustable sensitivity

### 🎮 Game Settings  
- **Resolution**: 800x600 (configurable)
- **FPS**: 60fps target
- **Lane Positions**: X = -5.0, 0.0, +5.0
- **Movement Speed**: Adjustable in control classes

## 🔧 Troubleshooting

### ❓ Common Issues

**Arduino not detected:**
- Check COM port in Device Manager
- Verify baud rate (115200)
- Install Arduino drivers
- Try different USB cable

**Joystick not responding:**
- Check wiring connections
- Verify 5V power supply
- Test with Arduino Serial Monitor
- Check threshold settings

**Game crashes:**
- Install all Python dependencies
- Check OpenGL support
- Verify texture files exist
- Run with admin privileges if needed

**Poor performance:**
- Close other applications
- Update graphics drivers
- Reduce resolution if needed
- Check Python version compatibility

## 🤝 Contributing

### 🛠️ Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test with both control methods
5. Submit pull request

### 📝 Code Style
- Follow PEP 8 for Python
- Comment hardware connections
- Include debug output for Arduino
- Test across different systems

## 📜 License

This project is open source and available under the MIT License.

## 🏆 Hackathon Project

Created for **Stormhacks** - combining software development with hardware innovation to create an immersive gaming experience that bridges physical and digital interaction.

### 🎯 Project Goals
- **Innovation**: Unique Arduino-based game controls
- **Accessibility**: Dual control options for all users  
- **Education**: Learn hardware-software integration
- **Fun**: Engaging 3D gameplay experience

---

**Built with ❤️ using Python, OpenGL, and Arduino**