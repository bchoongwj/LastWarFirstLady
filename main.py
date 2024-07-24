import pyautogui
import time
from icecream import ic
from datetime import datetime, timedelta
import os

# Get path directory of main file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Secretary images and names
images = [
    (os.path.join(script_dir, 'images', 'security.png'), 'strategy'),
    (os.path.join(script_dir, 'images', 'strategy.png'), 'security'),
    (os.path.join(script_dir, 'images', 'development.png'), 'development'),
    (os.path.join(script_dir, 'images', 'science.png'), 'science'),
    (os.path.join(script_dir, 'images', 'interior.png'), 'interior'),
]

# Miscellaneous images to click
accept_box_grey_image = (os.path.join(script_dir, 'images', 'accept_box_grey.png')),
accept_box_green_image = (os.path.join(script_dir, 'images', 'accept_box_green.png')),
confirmation_image = (os.path.join(script_dir, 'images', 'confirmation.png')),
appoint_image = (os.path.join(script_dir, 'images', 'appoint.png')),
decline_box_image = (os.path.join(script_dir, 'images', 'decline_box.png'))

# List of tasks and their intervals in seconds
tasks = [
    (lambda: main_appoint_secretary(*images[0]), 300),
    (lambda: main_appoint_secretary(*images[1]), 300),
    (lambda: main_appoint_secretary(*images[2]), 300),
    (lambda: main_appoint_secretary(*images[3]), 300),
    (lambda: main_appoint_secretary(*images[4]), 300)
]

# 3 second delay after running script for user to open window
initial_delay = 3
# Store the next execution times for each task
next_execution_times = [datetime.now() + timedelta(seconds=initial_delay) for _ in tasks]


# Main method to click on secretary, and appoint
def main_appoint_secretary(image, name):
    state = "Trying again now"

    try:
        ic("Checking for roles...")
        role = pyautogui.locateCenterOnScreen(image, confidence=0.9)

        if role:
            pyautogui.click(role)
            ic(f"Clicked: {name}")
            time.sleep(1)   # 1 second sleep to let game load


            if eligibility_check():
                scroll_list()
                accept_applicant()
                state = "Successful"
            else:
                pyautogui.press('esc')
                time.sleep(1.5)
                return "Check again soon"
        else:
            ic("No role found.")
            state = "Trying again now"
    except Exception as e:
        print(f"Error in find_role: {e}")
        state = "Trying again now"
    return state

# Checking if 5 minute cooldown is up. Useful for 1st run before intervals are set
def eligibility_check():
    try:
        # Uses appoint and red box button to check if cooldown is done
        ic("Checking if can appoint...")
        appoint_button = pyautogui.locateCenterOnScreen(appoint_image, confidence=0.9)
        decline_button = pyautogui.locateCenterOnScreen(decline_box_image, confidence=0.9)
        if appoint_button and decline_button:
            return True

    except Exception as e:
        print(f"Appointment still on cooldown: {e}")
        return False

# Scrolls to the top of applicant list
def scroll_list():
    try:
        # Click on grey box to ensure scrolling is done on game's list
        accept_box_grey = pyautogui.locateCenterOnScreen(accept_box_grey_image, confidence=0.9)
        if accept_box_grey:
            x, y = accept_box_grey
            new_x = x - 200
            ic("Moved mouse to grey accept box")
            pyautogui.click(new_x, y)

            # Scroll up
            for _ in range(6):
                pyautogui.scroll(250)  # Adjust the amount if necessary
                ic("scrolled")
                pyautogui.sleep(1)  # Small delay to ensure smooth scrolling

            ic("Scrolling completed")
        else:
            ic("Image not found on the screen.")
    except Exception as e:
        print(f"Error: {e}")

def accept_applicant():
    try:
        accept_box_green = pyautogui.locateCenterOnScreen(accept_box_green_image, confidence=0.9)
        ic("Green box found")
        if accept_box_green:
            pyautogui.click(accept_box_green)
            ic("Click green accept box")
            time.sleep(1)

            try:
                ic("Finding confirmation box")
                confirmation = pyautogui.locateCenterOnScreen(confirmation_image, confidence=0.9)
                if confirmation:
                    ic("Found confirmation box")
                    time.sleep(0.5)
                    pyautogui.click(confirmation)
                    ic("Clicked confirmation box")
                    ic("Accepted applicant")
                    pyautogui.press('esc')      # To go back to main secretary screen
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error in confirming application: {e}")

    except Exception as e:
        print(f"Error in finding green box: {e}")


# Runs main_appoint_secretary and sets interval based on result
def run_task(index):
    task, interval = tasks[index]
    success = task()  # Run the task and check if it was successful
    if success == "Successful":
        next_execution_times[index] = datetime.now() + timedelta(seconds=interval)  # Update the next execution time to 5 minutes only if successful
    elif success == "Trying again now":
        next_execution_times[index] = datetime.now() + timedelta(seconds=0)  # Keep trying till success
    elif success == "Check again soon":
        next_execution_times[index] = datetime.now() + timedelta(seconds=60)  # Update the next execution to be in 1 minute's time


# Main loop
while True:
    now = datetime.now()
    # Find the index of the task that should run next
    next_task_index = min(range(len(next_execution_times)), key=lambda i: next_execution_times[i])
    next_task_time = next_execution_times[next_task_index]

    # Calculate how long to sleep until the next task needs to run
    sleep_time = (next_task_time - now).total_seconds()

    # If the next task should run now or is overdue, run it immediately
    if sleep_time <= 0:
        run_task(next_task_index)
    else:
        # Sleep until the next task needs to run
        time.sleep(sleep_time)
