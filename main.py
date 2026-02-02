import cv2
from vision_module import process_frame
from control_module import calculate_pwm

def main():
    # --- SETUP ---
    cap = cv2.VideoCapture(0)
    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)
    
    # Calculate the center of the image (The robot's "nose")
    image_center_x = width // 2

    if not cap.isOpened():
        print("Error: Camera not found")
        return

    print("Line Follower Robot Started.")
    print("Features: Vision Processing (MPC Lookahead) | Dynamic Speed Control")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # --- 1. VISION PIPELINE ---
        # Get waypoints and curvature from our vision module
        mpc_waypoints, curvature, debug_thresh = process_frame(frame, width, height)

        # Draw waypoints for visualization
        for pt in mpc_waypoints:
            cv2.circle(frame, pt, 5, (0, 255, 0), -1)

        # --- 2. CONTROL LOGIC ---
        if len(mpc_waypoints) >= 3:
            # STEP A: Select Lookahead Point
            # We pick index 2 (the 3rd point). 
            # This lets us target ~150 pixels ahead of the robot.
            target_point = mpc_waypoints[2] 
            target_x = target_point[0]
            target_y = target_point[1]

            # Visual Debug: Draw a big RED circle on the Target Point
            cv2.circle(frame, (target_x, target_y), 10, (0, 0, 255), -1)
            
            # STEP B: Calculate Error
            # Error = How far RIGHT the target is from the center
            error = target_x - image_center_x
            
            # STEP C: Calculate PWM with Dynamic Speed
            # We pass the curvature to adjust base speed automatically
            l_pwm, r_pwm = calculate_pwm(error, curvature)

            # --- TERMINAL OUTPUT ---
            # Print status with \r to update in place
            # Showing Curvature (Curve) to verify dynamic speed logic
            # Added fixed width for Target X and trailing spaces to clear old text
            print(f"Target X: {target_x:3d} | Curve: {curvature:.5f} | PWM -> L: {l_pwm:4d}  R: {r_pwm:4d}      ", end='\r')

        # --- DISPLAY ---
        cv2.imshow("Advanced Control View", frame)
        # Optional: Show the thresholded view for debugging
        # cv2.imshow("Debug Thresh", debug_thresh) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
