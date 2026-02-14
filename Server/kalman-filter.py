import time

from adc import ADC

DELAY_MS = 1

class KalmanFilter:
    def __init__(self, Q, R, initial_state=0, initial_covariance=1000):
        self.Q = Q  # Process noise
        self.R = R  # Measurement noise
        self.x = initial_state  # State estimate
        self.P = initial_covariance  # Estimate covariance

    def predict(self):
        # Time update only
        self.P = self.P + self.Q
        return self.x

    def update(self, z):
        # Prediction step
        x_prior = self.x
        P_prior = self.P + self.Q

        # Update step
        K = P_prior / (P_prior + self.R)
        self.x = x_prior + K * (z - x_prior)
        self.P = (1 - K) * P_prior

        return self.x


if __name__ == "__main__":

    adc_controller = ADC()
    initial_voltage = adc_controller.read_battery_voltage_controller()
    print("Initial voltage: ", initial_voltage)
    kf = KalmanFilter(Q=0.01, R=0.1, initial_state=initial_voltage)

    for i in range(100):
        voltage_estimate = kf.predict()
        print(f"Value: {i}, Kalman Estimate      : {kf.predict()}")
        #print(f"Value: {i}, Kalman Update Output : {kf.update(adc_controller.read_battery_voltage_controller())}")
        time.sleep(DELAY_MS/100)
