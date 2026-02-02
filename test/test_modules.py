import sys
import os
import cv2
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vision_module import process_frame
from control_module import calculate_pwm

def test_logic():
    print("Testing Vision Module...")
    # Create a dummy image (black background with a white line)
    width, height = 640, 480
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a diagonal line (approximate curve)
    cv2.line(frame, (320, 480), (400, 200), (255, 255, 255), 10)
    
    waypoints, curvature, thresh = process_frame(frame, width, height)
    
    print(f"Waypoints detected: {len(waypoints)}")
    print(f"Curvature detected: {curvature}")
    
    if len(waypoints) > 0:
        print("Vision Module: PASS")
    else:
        print("Vision Module: WARN (No points found on dummy image)")

    print("\nTesting Control Module...")
    # Test straight line (low curvature)
    l_pwm, r_pwm = calculate_pwm(error=0, curvature=0.0)
    print(f"Straight Line (Curve 0.0) -> L: {l_pwm}, R: {r_pwm}")
    # Expect high speed (around 200 based on default)
    if l_pwm > 150 and r_pwm > 150:
         print("Dynamic Speed (Straight): PASS")
    else:
         print("Dynamic Speed (Straight): FAIL")

    # Test sharp curve + high error (Aggressive Turn)
    # Target is far right (error = 200), Kp = 1.5, base_speed = 60
    # turn_correction = 200 * 1.5 = 300
    # Left = 60 + 300 = 360 -> clamped to 250
    # Right = 60 - 300 = -240 (strong reverse!)
    l_pwm_curve, r_pwm_curve = calculate_pwm(error=200, curvature=0.005)
    print(f"Aggressive Turn (Error 200, Curve 0.005) -> L: {l_pwm_curve}, R: {r_pwm_curve}")
    if r_pwm_curve < -100:
        print("Aggressive Reverse Turn: PASS")
    else:
        print("Aggressive Reverse Turn: FAIL")

if __name__ == "__main__":
    test_logic()
