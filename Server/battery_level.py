# Import the Control class from the Control module
from control import Control
import led
import adc

# Creating object 'control' of 'Control' class.
c = Control()

def demo_movement():
    # Move forward in action mode 1 and gait mode 1
    for i in range(3):
        data = ['CMD_MOVE', '1', '0', '35', '10', '0']
        c.run_gait(data)  # Run gait with specified parameters

    # Move right in action mode 1 and gait mode 1
    for i in range(3):
        data = ['CMD_MOVE', '1', '35', '0', '10', '0']
        c.run_gait(data)  # Run gait with specified parameters

    # Move backward in action mode 2 and gait mode 2    
    for i in range(3):
        data = ['CMD_MOVE', '2', '0', '-35', '10', '10']
        c.run_gait(data)  # Run gait with specified parameters
        
    # Move right in action mode 2 and gait mode 2    
    for i in range(3):
        data = ['CMD_MOVE', '2', '35', '0', '10', '10']
        c.run_gait(data)  # Run gait with specified parameters

def main():
    print("Attempting to read voltage and output on LED...")

if __name__ == "__main__":
    main()
