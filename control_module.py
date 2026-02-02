def calculate_pwm(error, curvature, max_speed=200, min_speed=60):
    """
    Calculates Left and Right Motor PWM values based on error and path curvature.
    
    Args:
        error (int): Distance from center to target point.
        curvature (float): The 'a' coefficient from the polynomial fit, indicating curve sharpness.
        max_speed (int): Speed when the line is straight (up to 250).
        min_speed (int): Speed when the curve is sharp.
        
    Returns:
        tuple: (left_pwm, right_pwm)
    """
    # Dynamic Base Speed Calculation
    # Curvature typically ranges from 0 (straight) to ~0.005 (sharp turn).
    SHARP_CURVE_THRESHOLD = 0.005
    
    # Normalize curvature influence
    curve_factor = curvature / SHARP_CURVE_THRESHOLD
    curve_factor = min(curve_factor, 1.0)
    curve_factor = max(curve_factor, 0.0)
    
    # Linear interpolation: High curvature -> Low speed
    base_speed = int(max_speed - (curve_factor * (max_speed - min_speed)))
    
    # --- Steering Logic ---
    # Kp: Steering Sensitivity. 
    # Increased to 1.5 to ensure turn_correction > base_speed for sharp turns, 
    # enabling negative PWM (reverse) on the inner wheel.
    Kp = 0.8
    
    turn_correction = error * Kp
    
    # Differential Drive Mixing
    left_pwm = base_speed + turn_correction
    right_pwm = base_speed - turn_correction
    
    # Clamp values to -250 to 250 range
    # Negative values allow the motor to spin backwards for pivot turns.
    left_pwm = max(-250, min(250, int(left_pwm)))
    right_pwm = max(-250, min(250, int(right_pwm)))
    
    return left_pwm, right_pwm
