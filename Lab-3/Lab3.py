import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11
buzzer_pin = 18

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 100)
pwm.start(50)

def measure_distance():
    GPIO.output(PIN_TRIGGER, False)
    time.sleep(2)

    GPIO.output(PIN_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def distance_to_frequency(distance):
    min_distance = 2.0
    max_distance = 400.0
    min_frequency = 200
    max_frequency = 2000

    if distance < min_distance:
        distance = min_distance
    elif distance > max_distance:
        distance = max_distance

    frequency = min_frequency + (distance - min_distance) * (max_frequency - min_frequency) / (max_distance - min_distance)
    return round(frequency, 2)

try:
    while True:
        dist = measure_distance()
        freq = distance_to_frequency(dist)
        pwm.ChangeFrequency(freq)
        print(f"Measured Distance = {dist} cm, Playing Frequency = {freq} Hz")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    pwm.stop()
    GPIO.cleanup()
