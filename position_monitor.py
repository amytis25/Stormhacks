"""
Position Monitor for Game Objects
This file demonstrates how to get a constant stream of all object positions
"""

import json
import time
from base import App

class PositionMonitor:
    def __init__(self, app_instance):
        self.app = app_instance
        self.log_file = "position_log.txt"
        
    def save_positions_to_file(self):
        """Save current positions to a file"""
        positions = self.app.get_all_object_positions()
        
        with open(self.log_file, "a") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {json.dumps(positions, indent=2)}\n")
    
    def print_detailed_status(self):
        """Print detailed status of all objects"""
        positions = self.app.get_all_object_positions()
        
        print("\n" + "="*80)
        print(f"DETAILED POSITION REPORT - Frame {positions['frame']}")
        print("="*80)
        
        # Cube information
        cube = positions['cube']
        print(f"CUBE:")
        print(f"  Position: ({cube['x']:+6.2f}, {cube['y']:+6.2f}, {cube['z']:+6.2f})")
        print(f"  Rotation: {cube['rotation']:03.0f}°")
        print(f"  Lane: {cube['lane_name']} (index {cube['lane']})")
        print(f"  Movement State: {cube['movement_state']}")
        print(f"  Jumping: {cube['is_jumping']}, Crouching: {cube['is_crouching']}")
        
        # Pyramid information
        print(f"\nPYRAMID LEFT:")
        left = positions['pyramid_left']
        print(f"  Position: ({left['x']:+6.2f}, {left['y']:+6.2f}, {left['z']:+6.2f})")
        print(f"  Rotation: {left['rotation']:03.0f}°")
        
        print(f"\nPYRAMID RIGHT:")
        right = positions['pyramid_right']
        print(f"  Position: ({right['x']:+6.2f}, {right['y']:+6.2f}, {right['z']:+6.2f})")
        print(f"  Rotation: {right['rotation']:03.0f}°")
        
        # Performance information
        print(f"\nPERFORMANCE:")
        print(f"  FPS: {positions['fps']:.1f}")
        print(f"  Game Time: {positions['timestamp']/1000:.1f}s")

# Example usage function
def monitor_positions_example():
    """
    Example of how to continuously monitor positions
    This would run alongside your main game
    """
    print("Position monitoring example")
    print("This shows how you can access position data in real-time")
    print("\nTo use this in your main game, you can:")
    print("1. Call app.get_all_object_positions() at any time")
    print("2. Access control status with app.controls.get_control_status()")
    print("3. The position stream already prints to console every 10 frames")

if __name__ == "__main__":
    print("This file demonstrates position monitoring capabilities.")
    print("Run base.py to see the position streaming in action!")
    print("\nCurrent features:")
    print("- Constant position updates at 60 FPS")
    print("- Position streaming to console every 10 frames")
    print("- Detailed control status including movement states")
    print("- Lane tracking and movement animations")
    print("- Frame counting and performance monitoring")
