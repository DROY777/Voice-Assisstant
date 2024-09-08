import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Please say something:")
    audio = recognizer.listen(source)

try:
    # Convert audio to text
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
