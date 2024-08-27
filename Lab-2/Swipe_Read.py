import sys
import termios
import tty

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
    # Assuming the format is ;335004856=37232=02?
    start = card_data.find(';') + 1
    end = card_data.find('=')
    student_id = card_data[start:end]
    return student_id

if __name__ == "__main__":
    print("Please swipe your card...")
    card_data = get_card_data()
    print("Card data read:", card_data)
    student_id = extract_student_id(card_data)
    print("Extracted student ID:", student_id)
