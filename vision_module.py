import cv2
import numpy as np

def process_frame(frame, width, height):
    """
    Processes the image frame to detect the line, fit a curve, 
    and generate waypoints for the robot to follow.
    
    Returns:
        waypoints (list): List of (x, y) tuples representing the path.
        curvature (float): The 'a' coefficient of the quadratic fit (ax^2 + bx + c).
        debug_frame (numpy.ndarray): The processed frame (thresh) for debugging (optional).
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    pixel_points = cv2.findNonZero(thresh)

    waypoints = []
    curvature = 0.0

    if pixel_points is not None and len(pixel_points) > 500:
        x_vals = pixel_points[:, 0, 0]
        y_vals = pixel_points[:, 0, 1]

        try:
            # Fit the curve: x = ay^2 + by + c
            # curvature_coefficients = [a, b, c]
            curve_coefficients = np.polyfit(y_vals, x_vals, 2)
            poly_eqn = np.poly1d(curve_coefficients)
            
            # The 'a' coefficient represents the curvature/concavity
            curvature = abs(curve_coefficients[0])

            # Generate Waypoints
            num_points = 6
            step_size = 50 
            start_y = height - 20
            
            for i in range(num_points):
                curr_y = start_y - (i * step_size)
                if curr_y < 0: break
                curr_x = int(poly_eqn(curr_y))
                
                if 0 <= curr_x < width:
                    waypoints.append((curr_x, curr_y))
                    
        except Exception as e:
            # Curve fitting might fail if points are degenerate
            pass

    return waypoints, curvature, thresh
