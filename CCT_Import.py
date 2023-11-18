#This program and any related executables is the Intellectual Property of Nolan Young. Any attempts at recreation, reverse-engineering, or otherwise are subject to copywrite. 
import pyperclip
import keyboard
import pyautogui
import time
from rich.progress import Progress
from rich.progress import track
from colorama import Fore, Style
import colorama
import textwrap
colorama.init()
file_path = "README.md"

# Instructions on execution and dependencies loading
print(f"{Fore.CYAN}Dependencies loaded. Contact Nolan Young for more information. See the below change log.\n{Style.RESET_ALL}")
try:
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
readme = "README: This program works by copying and separating page names from numbers. After you're prompted for the number of plans and type of delimitation, you will have about 5 seconds to select the first entry in CCT. Due to the way the program operates, you will need to let it complete it's sequence before doing other work on your computer. Clicking away from CCT or otherwise interacting with the keyboard or mouse will cause it to fail."
print(textwrap.fill(readme,80))
print(f'{Fore.GREEN}\nPress CTRL+INS to start. Close CMD to kill the program.\n{Style.RESET_ALL}')

# Define main function
def handle_keypress():
    
    #Duplicate checker setup
    check = str("")
    check_count = int(0)
    
    # Notes and user input
    print(f'{Fore.RED}IMPORTANT - SORT PAGES BY NUMBER ASCENDING!!\n{Style.RESET_ALL}')
    try:
        pages = int(input("How many pages?\n"))
    except ValueError:
        print(f'{Fore.RED}Try again. Make sure to enter an integer. Program will restart.\n{Style.RESET_ALL}')
        handle_keypress()
        
    delim = input(f"What is your desired delimiter? (E.g. ; | _ | [space] )\nTip: the delimiter can be just about any special character(s) so long as it is\nconsistent in all pages and it first occurs between number and name.\n")
    print(
        f"{Fore.YELLOW}Set your text cursor in the first entry in less than 5 seconds{Style.RESET_ALL}"
    )
    
    # Waiting bar
    for _ in track(range(5), description="[magenta]Waiting..."):
        time.sleep(1)
        
    # Start timer for duration
    start = time.time()
    
    # Set progress bar function from class and start
    progress = Progress()
    progress.start()
    percent = progress.add_task(start= True, description="[green]Progress",
        total=pages)

    # Main Loop
    for _ in range(pages):
        # Copy the selected text to the clipboard
        time.sleep(0.1)
        pyautogui.hotkey('ctrl','a')
        time.sleep(0.13)
        pyautogui.hotkey('ctrl','c')
        time.sleep(0.13)
        
        
        # Retrieve the text from the clipboard
        clipboard_text = pyperclip.paste()
        
        #Checker while loop
        while clipboard_text == check :
            print(f'{Fore.RED}Copy error. Trying again.\n{Style.RESET_ALL}')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl','a')
            time.sleep(0.13)
            pyautogui.hotkey('ctrl','c')
            time.sleep(0.13)
            clipboard_text = pyperclip.paste()
            check_count = check_count + 1
            
        # Split the text into two strings delimited by var
        text_parts = clipboard_text.split(delim,1)
        #text_parts = clipboard_text.split(' ',1)

        # Check that the text can be split into two parts
        if len(text_parts) < 2:
            progress.stop()
            print(f"{Fore.LIGHTRED_EX}Not able to parse. Click hotkey to try again.\n\tTip: Check to make sure your page delimiter is present.{Style.RESET_ALL}")
            return
        

        #Returns the 2 parts of the string and prints progress
        progress.update(percent, advance=1)
        print(f"{Fore.LIGHTBLUE_EX}{text_parts[0]}{Style.RESET_ALL}")
        print(f"\t{text_parts[1]}")

        # Form entry
        entry(text_parts, 1, 'tab')
        entry(text_parts, 0, 'enter')

        # Field return to neutral
        keyboard.press_and_release('shift+tab')
        time.sleep(0.1)
        
        #Set Checker
        check = clipboard_text

    # End timer for duration and tell echo end of iteration with stats 
    end = time.time()
    progress.stop()
    print(
        f"{Fore.RED}Total number of errors = {str(check_count)}"
        f"{Fore.YELLOW}\nDone. Time elapsed: {Fore.GREEN}{str(round(end - start, 2))} (AVG Split: {str(round((end - start)/pages, 2))}){Fore.YELLOW} Seconds. Press hotkey to start again.{Style.RESET_ALL}"
    )
    

# Define page data entry
def entry(text_parts, arg1, arg2):
    keyboard.write(text_parts[arg1])
    time.sleep(0.1)
    keyboard.press_and_release(arg2)
    time.sleep(0.1)
    
# Create the keybinding
keyboard.add_hotkey('ctrl+insert', handle_keypress)

# Wait for the keybinding to be triggered
try:
    keyboard.wait()
except KeyboardInterrupt:
    print(f"{Fore.LIGHTRED_EX}Keyboard Interrupt. Click hotkey to try again.\n\tTip: Don't click away from CCT.\nWhen it asks you Y/N, enter N to restart.{Style.RESET_ALL}")
except ValueError:
    handle_keypress()