import speech_recognition as sr
import pyttsx3
import os
import subprocess
import psutil
import tkinter as tk
from tkinter import scrolledtext
import threading
from datetime import datetime

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice to female
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to open applications
def open_application(command):
    command = command.lower()
    log_message(f"Command received: {command}")

    if "notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen(["notepad.exe"])
    elif "calculator" in command or "calc" in command:
        speak("Opening Calculator")
        subprocess.Popen(["calc.exe"])
    elif "chrome" in command:
        speak("Opening Google Chrome")
        subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
    elif "spotify" in command:
        speak("Opening Spotify")
        subprocess.Popen(["C:/Users/YourUsername/AppData/Roaming/Spotify/Spotify.exe"])
    else:
        speak("Application not recognized")

# Function to provide the current time and day
def tell_time_day():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")  # Time in 12-hour format with AM/PM
    speak(f"it is {current_time}.")

def tell_day():
    now = datetime.now()
    current_day = now.strftime("%A")  # Day of the week 
    speak(f"Today is {current_day}")

def tell_date():
    now = datetime.now()
    current_date =now.strftime("%x")
    speak(f"Today is {current_date}")


# Function to log messages to the GUI
def log_message(message):
    log_area.config(state=tk.NORMAL)
    log_area.insert(tk.END, message + "\n")
    log_area.config(state=tk.DISABLED)
    log_area.yview(tk.END)

# Function to start the voice assistant
def start_voice_assistant():
    threading.Thread(target=voice_assistant_loop).start()

# Function for the voice assistant loop
def voice_assistant_loop():
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                log_message("Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                log_message(f"Recognized command: {command}")

                if "open" in command:
                     open_application(command)
                elif "hello" in command:
                     speak("Hello, how may I help you?")
                elif "how are you" in command:
                     speak("I'm fine, thank you.")
                elif "your name" in command:
                     speak("My name is Troy.")
                elif "what time is it" in command or "what's the time" in command or "time" in command:
                     tell_time_day()
                elif "date" in command or "what's the date" in command:
                     tell_date()     
                elif "day" in command or "what's the day" in command:
                     tell_day()          
                elif "exit" in command:
                     speak("Goodbye!")
                     break
                else:
                    speak("Sorry, I don't understand that command.")

        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            log_message("UnknownValueError - could not understand the audio.")
        except sr.RequestError as e:
            speak("Request error; please check your connection.")
            log_message(f"RequestError - {e}")

# Function to close the GUI application
def close_app():
    speak("Exiting application.")
    window.destroy()

# Create the main GUI window
window = tk.Tk()
window.title("Voice Assistant")
window.geometry("500x450")

# Set the background color to light blue
window.configure(bg="light blue")

# Add a heading in the center with an underline
heading = tk.Label(window, text="Voice Assistant", font=("Helvetica", 18, "underline"), bg="light blue")
heading.pack(pady=20)

# Create a frame to hold buttons side by side
button_frame = tk.Frame(window, bg="light blue")
button_frame.pack(pady=10)

# Create the start button and exit button inside the frame
start_button = tk.Button(button_frame, text="Start Voice Assistant", command=start_voice_assistant)
start_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=close_app)
exit_button.pack(side=tk.LEFT, padx=10)

# Create a log area to display recognized commands
log_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
log_area.pack(pady=10)

# Run the GUI event loop
window.mainloop()
