import RPi.GPIO as GPIO
import socket

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
buzzer_pin = 18
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 100)
pwm.start(50)

def distance_to_frequency(distance):
    # Define the mapping between distance and frequency
    min_distance = 2.0
    max_distance = 400.0
    min_frequency = 200
    max_frequency = 2000

    # Limit the distance within the valid range
    if distance < min_distance:
        distance = min_distance
    elif distance > max_distance:
        distance = max_distance

    # Calculate the frequency based on the distance
    frequency = min_frequency + (distance - min_distance) * (max_frequency - min_frequency) / (max_distance - min_distance)
    return round(frequency, 2)

try:
    # Allow user to input the port number to listen on
    port = int(input("Enter the port number to listen on: "))

    # Create a TCP server to wait for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print(f"Listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                # Receive distance data and play the corresponding frequency
                data = conn.recv(1024)
                if not data:
                    break
                distance = float(data.decode())
                frequency = distance_to_frequency(distance)
                pwm.ChangeFrequency(frequency)
                print(f"Received Distance = {distance} cm, Playing Frequency = {frequency} Hz")

except KeyboardInterrupt:
    print("Playback stopped by User")
    pwm.stop()
    GPIO.cleanup()
except Exception as e:
    print(f"Error: {e}")
    GPIO.cleanup()
