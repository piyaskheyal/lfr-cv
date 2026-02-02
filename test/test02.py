import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0)

    # Resolution
    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)

    if not cap.isOpened():
        print("Error: Camera not found")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Image Processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Invert Threshold: Detect BLACK line on light surface
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # 2. Get all white pixels
        pixel_points = cv2.findNonZero(thresh)

        if pixel_points is not None and len(pixel_points) > 500:
            
            x_vals = pixel_points[:, 0, 0]
            y_vals = pixel_points[:, 0, 1]

            # 3. Fit a 2nd Degree Polynomial
            try:
                curve_coefficients = np.polyfit(y_vals, x_vals, 2)
                poly_eqn = np.poly1d(curve_coefficients)

                # 4. Generate the 6 MPC Waypoints
                num_points = 6
                step_size = 50 
                start_y = height - 20
                
                mpc_waypoints = [] 

                for i in range(num_points):
                    curr_y = start_y - (i * step_size)
                    
                    if curr_y < 0:
                        break

                    curr_x = int(poly_eqn(curr_y))

                    # Bounds check
                    if 0 <= curr_x < width:
                        mpc_waypoints.append((curr_x, curr_y))
                        
                        # Draw circle
                        cv2.circle(frame, (curr_x, curr_y), 5, (0, 255, 0), -1)
                        
                        # FIX: Draw line using list indexing
                        if len(mpc_waypoints) > 1:
                            prev_pt = mpc_waypoints[-2]
                            curr_pt = mpc_waypoints[-1]
                            cv2.line(frame, prev_pt, curr_pt, (0, 255, 255), 2)
            
            except Exception as e:
                pass 

        cv2.imshow("MPC Prediction Horizon", frame)
        # cv2.imshow("Threshold", thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()