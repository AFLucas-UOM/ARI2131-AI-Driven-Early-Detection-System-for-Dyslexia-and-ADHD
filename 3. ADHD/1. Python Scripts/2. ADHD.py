import time
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

# Constants for configuration
MOUSE_MOVEMENT_THRESHOLD = 2  # Minimum horizontal mouse movement to be recorded as "left to right" movement
PROGRAM_DURATION_SECONDS = 300  # Duration in seconds to run the program
ADHD_WARNING_THRESHOLD = 5  # Number of fidgeting intervals to trigger a warning

# Variables to store user activity and ADHD-related data
activity = []  # Stores (timestamp, action) pairs
fidget_intervals = []  # Stores (start_time, end_time) of fidgeting intervals
fidget_count = 0  # Count of fidgeting intervals
last_mouse_x = None  # Variable to track the last mouse position
adhd_warning_triggered = False  # Flag to track if the warning has been triggered
burst_count = 0  # Count of bursts of activity
consecutive_bursts = 0
consecutive_actions = 0
last_action = None
start_time = 0
consecutive_key_presses = 0

def on_click(x, y, button, pressed):
    """Handle mouse input."""
    timestamp = time.time()
    action = "Mouse Press" if pressed else "Mouse Release"
    activity.append((timestamp, action))
    print(action)

    global burst_count, last_action, consecutive_bursts

    if action == "Mouse Release" and last_action == "Mouse Press":
        consecutive_bursts += 1
    else:
        consecutive_bursts = 0

    last_action = action

    if consecutive_bursts >= 4:
        burst_count += 1
        if burst_count == 4:
            print(f"Burst Detected: {burst_count} bursts")
            burst_count = 0

def on_key_press(key):
    """Handle keyboard input."""
    timestamp = time.time()
    action = f"Key Press: {key}"
    activity.append((timestamp, action))
    print(action)

    global burst_count, consecutive_actions, last_action, consecutive_key_presses

    if action == last_action:
        consecutive_actions += 1
    else:
        consecutive_actions = 1

    if consecutive_actions >= 3:
        burst_count += 1
        print(f"Burst Detected: {burst_count} bursts")
        consecutive_actions = 0

    last_action = action


def on_mouse_move(x, y):
    """Handle mouse movement."""
    global last_mouse_x
    if last_mouse_x is None:
        last_mouse_x = x
        return
    mouse_movement = abs(x - last_mouse_x)
    if mouse_movement >= MOUSE_MOVEMENT_THRESHOLD:
        timestamp = time.time()
        action = f"Mouse Move: {last_mouse_x} to {x}"
        activity.append((timestamp, action))
        last_mouse_x = x
        print(action)

def detect_fidget_intervals():
    """Fidget Intervals."""
    global fidget_count, fidget_intervals, activity
    fidget_start_time = None
    fidget_action_count = 0

    for timestamp, action in activity:
        # Define your criteria for fidgeting actions here
        if is_fidgeting_action(action):
            if fidget_start_time is None:
                fidget_start_time = timestamp
            fidget_action_count += 1
        else:
            if fidget_start_time is not None:
                if fidget_action_count >= MIN_FIDGET_ACTIONS:
                    fidget_intervals.append((fidget_start_time, timestamp))
                    fidget_count += 1
                fidget_start_time = None
                fidget_action_count = 0

    # Check if the last interval is a fidgeting interval
    if fidget_start_time is not None and fidget_action_count >= MIN_FIDGET_ACTIONS:
        fidget_intervals.append((fidget_start_time, timestamp))
        fidget_count += 1

def is_fidgeting_action(action):
    fidget_keywords = ["Mouse Press", "Mouse Release", "Key Press", "Mouse Move"]
    return action in fidget_keywords


# Constants for fidget detection
MIN_FIDGET_ACTIONS = 2  # Minimum number of fidgeting actions to constitute an interval

def create_pdf_report():
    """Create a PDF report."""
    c = canvas.Canvas('user_activity_report.pdf', pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 14)
    c.drawString(100, height - 50, "User Activity Report")

    total_fidgeting_time = sum(end - start for start, end in fidget_intervals)
    c.drawString(100, height - 100, f"Total fidgeting time: {total_fidgeting_time:.3f} seconds")
    c.drawString(100, height - 120, f"Number of fidgeting intervals: {fidget_count}")
    c.drawString(100, height - 140, f"Number of bursts of activity: {burst_count}")

    if (burst_count > 5) or (total_fidgeting_time > 10) or (fidget_count > 10):
        result_color = "red"
        assessment = "may have ADHD"
    else:
        result_color = "green"
        assessment = "doesn't have signs of ADHD"
    c.setFillColor(result_color)
    c.drawString(100, height - 180, f"The user {assessment}.")
    graph_image_path = 'user_activity.png'
    c.drawImage(graph_image_path, 100, height - 400, width=400, height=200)
    c.save()


# Main project Logic
def main():
    global  start_time   # Define start_time as a global variable

    start_time = time.time()  # Set the start_time when the program starts

    print("Logger: SETUP VIDEO TIME")
    time.sleep(2)
    print("Logger: RECORDING INPUT")

    # Initialize keyboard listener and mouse movement listener
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    # Initialize mouse listener to capture both click and move events
    mouse_listener = MouseListener(on_click=on_click, on_move=on_mouse_move)

    # Start keyboard and mouse listeners
    keyboard_listener.start()
    mouse_listener.start()

    try:
        start_time = time.time()
        while True:
            if time.time() - start_time >= PROGRAM_DURATION_SECONDS:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # Stop listeners when the program duration is over
    keyboard_listener.stop()
    mouse_listener.stop()

    # Detect fidgeting intervals
    detect_fidget_intervals()

    # Create and save the graph image
    timestamps, actions = zip(*activity)
    plt.figure(figsize=(10, 6))
    for i in range(1, len(timestamps)):
        plt.plot([timestamps[i - 1], timestamps[i]], [i - 1, i], 'b-')

    plt.yticks(range(len(timestamps)), actions, fontsize=8)
    plt.xlabel('Timestamp')
    plt.title('User Activity Over Time')
    plt.tight_layout()
    plt.savefig('user_activity.png')

    # Create and save the PDF report
    print("Saving PDF report...")
    create_pdf_report()
    print("PDF report saved.")

if __name__ == "__main__":
    main()