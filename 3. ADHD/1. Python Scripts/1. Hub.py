import webbrowser
import time
import subprocess
import sys

# Define the video links for each subject
video_links = {
    "Biology": "https://www.youtube.com/watch?v=tZE_fQFK8EY&ab_channel=CrashCourse",
    "Chemistry": "https://www.youtube.com/watch?v=FSyAehMdpyI&list=PL8dPuuaLjXtPHzzYuWy6fYEaX9mQQ8oGr&index=2&ab_channel=CrashCourse",
    "Physics": "https://www.youtube.com/watch?v=kKKM8Y-u7ds&list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV&index=6&ab_channel=CrashCourse",
    "History": "https://www.youtube.com/watch?v=m19F4IHTVGc&t=5s&ab_channel=HistoryonMaps",
    "Maths": "https://www.youtube.com/watch?v=eVm063xmnow&ab_channel=TED-Ed",
    "Environmental": "https://www.youtube.com/watch?v=RoIpCJwX7-M&ab_channel=HotMess",
    "Engineering": "https://www.youtube.com/watch?v=u-xjja6mK2k&ab_channel=ConcerningReality",
    "Computing": "https://www.youtube.com/watch?v=R9OHn5ZF4Uo&ab_channel=CGPGrey",
    "Accounts": "https://www.youtube.com/watch?v=yYX4bvQSqbo&ab_channel=AccountingStuff",
    "Economics": "https://www.youtube.com/watch?v=3ez10ADR_gM&ab_channel=CrashCourse"
}

# Function to open the selected video
def open_video(selected_subject):
    if selected_subject in video_links:
        print(f"{selected_subject} video loading...")
        time.sleep(2)  # Wait for 2 seconds

        try:
            webbrowser.open(video_links[selected_subject], new=2, autoraise=True)
        except Exception as e:
            print(f"Error opening the browser. Here is the video link: {video_links[selected_subject]}")
    else:
        print(f"Sorry, we don't have a video for {selected_subject}.")

# Function to run ADHD.py in a separate process
def run_adhd_script():
    try:
        python_executable = sys.executable
        subprocess.run([python_executable, "ADHD.py"])
    except Exception as e:
        print(f"Error running ADHD.py: {e}")

# Display the list of subjects for the user to choose from
def display_subjects():
    print("Choose your favorite subject:")
    for i, subject in enumerate(video_links.keys(), 1):
        print(f"{i}. {subject}")

# Main program logic
def main():
    display_subjects()

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            subjects = list(video_links.keys())
            if 1 <= choice <= len(subjects):
                selected_subject = subjects[choice - 1]
                open_video(selected_subject)

                # Run ADHD.py in a separate process
                run_adhd_script()
                time.sleep(30)  # Wait for 30 seconds

                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()