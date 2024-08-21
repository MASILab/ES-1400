import sys
import termios
import tty
import RPi.GPIO as GPIO
import time
import getpass

# Motor control setup
GPIO.setmode(GPIO.BCM)
servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def get_card_data():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    card_data = ""
    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            char = sys.stdin.read(1)
            if char == '\r' or char == '\n':  # End of data
                break
            card_data += char
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return card_data

def extract_student_id(card_data):
    start = card_data.find(';') + 1
    end = card_data.find('=')
    student_id = card_data[start:end]
    return student_id

def set_custom_password():
    password = getpass.getpass("Please set a custom password for your safe box: ")
    confirm_password = getpass.getpass("Please re-enter the password to confirm: ")

    while password != confirm_password:
        print("Passwords do not match. Please try again.")
        password = getpass.getpass("Please set a custom password for your safe box: ")
        confirm_password = getpass.getpass("Please re-enter the password to confirm: ")

    print("Your password has been set. Please remember it for future use.")
    return password

def set_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle(0)

def validate_id_and_password(stored_student_id, correct_password):
    try:
        print("Please swipe your card again to verify the student ID...")
        card_data = get_card_data()
        student_id = extract_student_id(card_data)

        if student_id.strip() == stored_student_id.strip():
            print("Student ID matches!")

            # Prompt for password input
            password = getpass.getpass("Please enter the custom password: ")

            if password == correct_password:
                print("Password is correct!")
                print("Verification successful.")
                
                # Control motor
                print("Activating motor...")
                set_angle(90)  # Move motor to 90 degrees
                time.sleep(2)  # Hold position for 2 seconds
            else:
                print("Incorrect password. Verification failed.")
        else:
            print("Student ID does not match. Verification failed.")
    finally:
        if GPIO.getmode() is not None:
            pwm.stop()
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        # Step 1: Get the card data and extract the student ID
        print("Please swipe your card...")
        card_data = get_card_data()
        print("Card data read:", card_data)
        student_id = extract_student_id(card_data)
        print("Extracted student ID:", student_id)

        # Step 2: Set a custom password for future verification
        password = set_custom_password()

        # Step 3: Validate the student ID and password, then control the motor if successful
        validate_id_and_password(student_id, password)

    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        if GPIO.getmode() is not None:
            pwm.stop()
            GPIO.cleanup()
