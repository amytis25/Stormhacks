# Force Cube Runner - Arduino Edition

A 3D obstacle avoidance game built with Python, OpenGL, and Arduino controls. Navigate through lanes while dodging obstacles using joystick controls and ultrasonic sensor movements!

## Game Overview

**Force Cube Runner** is an immersive 3D game where players control a cube navigating through three lanes while avoiding moving obstacles. The game features both traditional keyboard controls and innovative Arduino hardware controls for a unique gaming experience.

### Core Gameplay
- **Lane Navigation**: Move between left, center, and right lanes
- **Vertical Movement**: Duck under or jump over obstacles
- **Obstacle Avoidance**: Avoid spheres and wall obstacles
- **Survival Timer**: Track how long you survive
- **Progressive Difficulty**: Obstacles move faster over time

## Control Options

### Keyboard Controls (Always Available)
**Movement Controls:**
- **LEFT Arrow/A**: Move to left lane
- **RIGHT Arrow/D**: Move to right lane  
- **UP Arrow/W**: Jump over obstacles
- **DOWN Arrow/S**: Crouch under obstacles

**Camera Controls (Added Feature):**
- **Q**: Move camera left
- **E**: Move camera right
- **Z**: Move camera up
- **C**: Move camera down
- **X**: Move camera forward
- **V**: Move camera backward
- **G**: Reset camera position

**Game Controls:**
- **R**: Reset timer
- **P**: Pause/resume timer

### Arduino Hardware Controls (`base_arduino.py`)
- **Joystick X-axis**: Switch between lanes (left/center/right)
- **Ultrasonic Sensor**: Control height (close = crouch, far = jump)
- **Real-time positioning**: Smooth continuous movement based on distance
- **Automatic fallback**: Switches to keyboard if Arduino disconnects

## Hardware Setup (Arduino)

### Required Components
- **Arduino Uno/Nano**
- **Analog Joystick Module**
- **HC-SR04 Ultrasonic Sensor**
- **Jumper wires**
- **Breadboard**

### Wiring Diagram
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

### Arduino Code
Upload `game_controller_combined.ino` to your Arduino:
- Reads both joystick and ultrasonic sensor
- Sends formatted data to Python game
- 115200 baud rate communication

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+
- **Python**: Python 3.7 or higher (tested with Python 3.9.13)
- **RAM**: 2GB minimum, 4GB recommended
- **Graphics**: OpenGL 3.0+ compatible graphics card
- **USB Port**: Available for Arduino connection (if using hardware controls)

### Python Dependencies
Install all required packages using pip:

```bash
# Core game engine dependencies
pip install pygame>=2.0.0
pip install PyOpenGL>=3.1.0
pip install PyOpenGL-accelerate>=3.1.0

# Arduino communication (for hardware controls)
pip install pyserial>=3.4

# Additional dependencies
pip install pillow>=8.0.0
pip install numpy>=1.19.0
```

**Or install all at once:**
```bash
pip install pygame PyOpenGL PyOpenGL-accelerate pyserial pillow numpy
```

### Required Files
This game includes the following essential files:
- **Main Game**: `base_arduino.py` (primary game with Arduino support)
- **Control Systems**: `controls.py`, `arduino_controls.py`
- **Graphics Rendering**: `shapes.py`, `lane_markers.py`, `game_timer.py`
- **Game Logic**: `sphere_manager.py`, `leaderboard.py`
- **User Interface**: `arduino_start_screen.py`, `start_screen.py`, `button.py`
- **Arduino Firmware**: `game_controller_combined/game_controller_combined.ino`
- **Assets**: `MrElectric.png` (sphere texture)

## Getting Started

### Installation Steps

1. **Install Python 3.7+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure pip is included during installation
   - Verify installation: `python --version`

2. **Install Required Dependencies**
   ```bash
   # Install all required packages
   pip install pygame PyOpenGL PyOpenGL-accelerate pyserial pillow numpy
   
   # Verify installation
   python -c "import pygame, OpenGL.GL, serial, PIL, numpy; print('All dependencies installed successfully!')"
   ```

3. **Download Game Files**
   - Clone or download this repository
   - Ensure all Python files are in the same directory
   - Verify `MrElectric.png` asset file is present

4. **Arduino Setup (Optional)**
   - Connect Arduino hardware (see Hardware Setup section)
   - Upload `game_controller_combined.ino` using Arduino IDE
   - Test connection with Arduino Serial Monitor

### Running the Game

#### Standard Version (Keyboard + Arduino Auto-Detection)
```bash
# Run Force Cube Runner with automatic Arduino detection
python base_arduino.py
```

The game will automatically:
- Test for Arduino connection on startup  
- Display connection status on the start screen
- Allow you to choose between Arduino or Keyboard controls
- Fall back to keyboard if Arduino is not detected

#### Quick Start (No Arduino Required)
Even without Arduino hardware, you can play using keyboard controls:
- The game automatically detects if Arduino is not connected
- Falls back to keyboard controls seamlessly
- All gameplay features remain available

### First Time Checklist
- [ ] Python 3.7+ installed and working
- [ ] All pip dependencies installed successfully
- [ ] Game files downloaded to same directory
- [ ] `MrElectric.png` texture file present
- [ ] Arduino connected and programmed (optional)
- [ ] Run `python base_arduino.py` to start

### Dependency Verification

After installing dependencies, verify everything is working:

```bash
# Test Python and basic imports
python -c "import sys; print(f'Python {sys.version}')"

# Test game dependencies
python -c "
import pygame
import OpenGL.GL
import serial
import PIL
import numpy
print('✓ All dependencies imported successfully!')
print(f'✓ Pygame version: {pygame.version.ver}')
print(f'✓ PyOpenGL installed and working')
print(f'✓ PySerial ready for Arduino communication')
"

# Test game files
python -c "
import os
files = ['base_arduino.py', 'controls.py', 'arduino_controls.py', 'MrElectric.png']
missing = [f for f in files if not os.path.exists(f)]
if missing:
    print(f'✗ Missing files: {missing}')
else:
    print('✓ All essential game files present')
"
```

If all tests pass, you're ready to run the game!

## Features

## Features

### Visual Elements
- **3D OpenGL Graphics**: Smooth 60fps rendering with modern OpenGL
- **Textured Obstacles**: Sphere obstacles with electric-themed textures  
- **Lane Markers**: Clear visual guides for navigation
- **Professional UI**: Clean, emoji-free interface design
- **Real-time Timer**: Survival time display (MM:SS:mmm format)
- **Camera System**: 7-key camera control system (Q/E/Z/C/X/V/G)

### Game Mechanics
- **Collision Detection**: Precise 3D collision system between player and obstacles
- **Three-Lane Movement**: Strategic lane switching gameplay
- **Height-based Avoidance**: Jump/crouch mechanics for vertical obstacles
- **Progressive Difficulty**: Dynamic obstacle generation with increasing challenge
- **Game Over System**: Instant restart with time display
- **Dual Control Support**: Seamless switching between Arduino and keyboard

### Arduino Integration
- **Automatic Detection**: Boot-time Arduino connection testing
- **Hardware Controls**: Real-time joystick and ultrasonic sensor input
- **Smooth Movement**: Continuous position interpolation from sensor data
- **Intelligent Fallback**: Automatic keyboard backup when Arduino disconnects
- **Status Feedback**: Clean connection status display (no clutter)
- **Professional Interface**: Removed emoji messaging for clean presentation

## Architecture

### File Structure
```
Stormhacks/
├── base_arduino.py             # Main game with Arduino support
├── controls.py                 # Keyboard control system
├── arduino_controls.py         # Arduino hardware interface
├── shapes.py                   # 3D object rendering (cubes, spheres)
├── sphere_manager.py           # Obstacle generation and management
├── lane_markers.py             # Visual lane guides rendering
├── game_timer.py               # HUD timer display system
├── arduino_start_screen.py     # Arduino-enabled start screen
├── start_screen.py             # Standard start screen
├── button.py                   # UI button components
├── leaderboard.py              # Score tracking system
├── position_monitor.py         # Debug position monitoring
├── game_controller_combined/   # Arduino firmware directory
│   └── game_controller_combined.ino  # Arduino sketch
├── MrElectric.png              # Sphere texture asset
├── .gitignore                  # Git ignore file
└── README.md                   # This documentation
```

### Game Flow
1. **Start Screen** → Choose control method (Arduino/Keyboard)
2. **Connection Test** → Automatic Arduino detection
3. **Control Instructions** → 5-second countdown with control guide
4. **Game Setup** → Initialize OpenGL, controls, objects
5. **Main Loop** → Handle input, update physics, render
6. **Collision Check** → Detect obstacle hits
7. **Game Over** → Show final time, return to start

## Configuration

### Arduino Settings
- **Port**: Default COM3 (Windows) - modify in code if needed
- **Baud Rate**: 115200
- **Sensor Ranges**: 5-50cm for ultrasonic positioning
- **Joystick Threshold**: Adjustable sensitivity

### Game Settings  
- **Resolution**: 800x600 (configurable)
- **FPS**: 60fps target
- **Lane Positions**: X = -4.0, 0.0, +4.0
- **Movement Speed**: Adjustable in control classes

## Troubleshooting

### Common Issues

**Python Dependencies Missing:**
```bash
# Error: ModuleNotFoundError: No module named 'pygame'
pip install pygame PyOpenGL PyOpenGL-accelerate pyserial pillow numpy

# Verify installation
python -c "import pygame, OpenGL.GL, serial; print('Dependencies OK')"
```

**Arduino not detected:**
- Check COM port in Device Manager (Windows)
- Verify baud rate (115200) in Arduino Serial Monitor
- Install Arduino drivers if needed
- Try different USB cable/port
- Test Arduino code separately first

**OpenGL/Graphics Issues:**
```bash
# Error: OpenGL not supported
# Update graphics drivers
# Install Microsoft Visual C++ Redistributable
# Try running as administrator
```

**Game crashes on startup:**
- Ensure Python 3.7+ is installed
- Install all dependencies with pip
- Check that `MrElectric.png` exists in game directory
- Verify OpenGL 3.0+ support on your system

**Joystick not responding:**
- Check Arduino wiring connections (see Hardware Setup)
- Verify 5V power supply to joystick
- Test with Arduino Serial Monitor: `Tools > Serial Monitor`
- Check threshold settings in `arduino_controls.py`

**Poor performance/low FPS:**
- Close other applications
- Update graphics drivers  
- Check Windows graphics settings (prefer high performance)
- Reduce screen resolution if needed

## Contributing

### Development Setup
1. **Fork the repository** on GitHub
2. **Clone locally**: `git clone <your-fork-url>`
3. **Install dependencies**: `pip install pygame PyOpenGL PyOpenGL-accelerate pyserial pillow numpy`
4. **Test installation**: Run dependency verification script above
5. **Create feature branch**: `git checkout -b feature-name`
6. **Make changes** and test thoroughly
7. **Test with both control methods** (keyboard and Arduino if available)
8. **Submit pull request** with detailed description

### Development Guidelines
- **Follow PEP 8** Python style guidelines
- **Comment hardware connections** in Arduino-related code
- **Include debug output** for Arduino communication
- **Test across different systems** (Windows/Mac/Linux if possible)
- **Verify all dependencies** are properly documented
- **Maintain backward compatibility** with existing save files
- **Update README** if adding new features or dependencies

### Testing Checklist
Before submitting changes:
- [ ] Game starts without errors
- [ ] Keyboard controls work correctly
- [ ] Arduino detection works (if hardware available)
- [ ] No new dependency requirements (or properly documented)
- [ ] Camera controls function properly
- [ ] Game over/restart mechanics work
- [ ] Professional UI maintained (no emoji, clean interface)
- [ ] Performance remains smooth (60fps target)

## License

This project is open source and available under the MIT License.

## Hackathon Project

Created for **Stormhacks** - combining software development with hardware innovation to create an immersive gaming experience that bridges physical and digital interaction.

### Project Goals
- **Innovation**: Unique Arduino-based game controls
- **Accessibility**: Dual control options for all users  
- **Education**: Learn hardware-software integration
- **Fun**: Engaging 3D gameplay experience

---

**Built with Python, OpenGL, and Arduino**