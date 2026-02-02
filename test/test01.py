import cv2
import numpy as np

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Pre-processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Threshold (Adjust '60' if needed)
        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # Find Contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest_contour) > 1000:
                
                # A. Draw Contour
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

                # B. Draw Bounding Rect
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
                # C. Get Trajectory Line
                # .flatten() makes these simple floats, not arrays
                vx, vy, x, y = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01).flatten()

                x = int(x)
                y = int(y)
                length = 200 

                p1 = (int(x - vx * length), int(y - vy * length))
                p2 = (int(x + vx * length), int(y + vy * length))
                cv2.line(frame, p1, p2, (255, 0, 0), 2)
                
                # Calculate Heading Angle
                angle_rad = np.arctan2(vy, vx)
                angle_deg = np.degrees(angle_rad)
                
                if angle_deg < 0: angle_deg += 180 

                # FIX: Removed [0] because angle_deg is now a simple float
                cv2.putText(frame, f"Angle: {angle_deg:.1f}", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow('Line Detection (Final)', frame)
        cv2.imshow('Mask (Debug)', thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()