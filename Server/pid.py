
class Incremental_PID:
    """
    Incremental PID (Proportional-Integral-Derivative) controller.

    This class implements a PID controller with anti-windup on the integral term.
    It calculates the control output needed to drive a system's feedback value 
    toward a desired target value (setpoint).

    Attributes:
        target_value (float): Desired setpoint the controller will attempt to reach.
        kp (float): Proportional gain.
        ki (float): Integral gain.
        kd (float): Derivative gain.
        last_error (float): Error from the previous calculation (used for derivative).
        p_error (float): Current proportional term.
        i_error (float): Accumulated integral term (limited by i_saturation).
        d_error (float): Current derivative term.
        i_saturation (float): Maximum absolute value allowed for the integral term.
        output (float): Last computed PID output.

    Methods:
        pid_calculate(feedback_val):
            Compute the PID output given the current system feedback.
        set_kp(proportional_gain):
            Set the proportional gain (kp).
        set_ki(integral_gain):
            Set the integral gain (ki).
        set_kd(derivative_gain):
            Set the derivative gain (kd).
        set_i_saturation(saturation_val):
            Set the maximum absolute value for the integral term.
        set_target_value(target):
            Set a new target value (setpoint) for the controller.

    Usage Example:
        pid = Incremental_PID(P=1.0, I=0.1, D=0.05)
        pid.set_target_value(100)

        feedback = 0
        output = pid.pid_calculate(feedback)
    """

    def __init__(self, P=0.0, I=0.0, D=0.0):
        self.target_value = 0.0
        self.kp = P
        self.ki = I
        self.kd = D
        self.last_error = 0.0
        self.p_error = 0.0
        self.i_error = 0.0
        self.d_error = 0.0
        self.i_saturation = 10.0
        self.output = 0.0

    def pid_calculate(self, feedback_val):
        error = self.target_value - feedback_val
        self.p_error = self.kp * error
        self.i_error += error 
        self.d_error = self.kd * (error - self.last_error)
        if (self.i_error < -self.i_saturation):
            self.i_error = -self.i_saturation
        elif (self.i_error > self.i_saturation):
            self.i_error = self.i_saturation
        self.output = self.p_error + (self.ki * self.i_error) + self.d_error
        self.last_error = error
        return self.output

    def set_kp(self, proportional_gain):
        self.kp = proportional_gain

    def set_ki(self, integral_gain):
        self.ki = integral_gain

    def set_kd(self, derivative_gain):
        self.kd = derivative_gain

    def set_i_saturation(self, saturation_val):
        self.i_saturation = saturation_val

    def set_target_value(self, target):
        self.target_value = target