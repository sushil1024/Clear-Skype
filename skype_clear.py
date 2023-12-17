import csv
from skpy import Skype
import time
import sys

username = str(input("Enter skype username (ie. something@example.com): "))
password = str(input("Enter skype password (ie. somepassword_123): "))

csv_file_path = "skype_groups_logs.csv"

ch = input("Are you sure to leave from all groups? (y/n): ")

# spinning cursor
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def print_with_spinner(text, spinner):
    sys.stdout.write(f"{text} {next(spinner)}")
    sys.stdout.flush()
    sys.stdout.write("\b" * (len(text) + 2))  # Move the cursor back

try:
    # Log in to Skype
    sk = Skype(username, password)

except Exception as e:
    exit(f"Error occured at login: {e}")

if ch.lower() != 'y':
    exit("Aborting!..")

else:
    spinner = spinning_cursor()

    # Get the list of all groups
    groups = sk.chats.recent()

    try:
        with open(csv_file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            cnt = 0
            # Leave each group
            for group_id in groups:
                cnt += 1
                chat = sk.chats.chat(group_id)
                
                # print(f"Leaving group and clearing messages: {cnt}")
                print_with_spinner(f"Leaving group and clearing messages! ", spinner)

                # Clear messages and leave groups
                chat.delete()
                try:
                    chat.leave()
                except:
                    pass

                if cnt < 2:
                    status = 'Done'
                    csv_writer.writerow([username, status])

                time.sleep(0.1)
    
    except Exception as e:
        print(f"Error occured while leaving groups: {e}")
        print("Verify once from skype. Also check skype_groups_logs.csv")

input()