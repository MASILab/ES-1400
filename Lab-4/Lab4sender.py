import RPi.GPIO as GPIO
import time
import socket

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

def measure_distance():
    # Initialize the trigger pin and wait for the sensor to settle
    GPIO.output(PIN_TRIGGER, False)
    time.sleep(2)

    # Send a pulse to trigger the ultrasonic sensor
    GPIO.output(PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, False)

    # Wait for the echo response and record the start time
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()

    # Record the end time when the echo is received
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance based on the pulse duration
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    # Allow user to input the receiver's IP address and port
    receiver_ip = input("Enter the receiver's IP address: ")
    port = int(input("Enter the port number: "))

    # Create a connection to the receiver
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((receiver_ip, port))
        while True:
            # Measure distance and send data
            dist = measure_distance()
            s.sendall(str(dist).encode())
            print(f"Measured Distance = {dist} cm, Data sent to receiver.")
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
except Exception as e:
    print(f"Error: {e}")
    GPIO.cleanup()
