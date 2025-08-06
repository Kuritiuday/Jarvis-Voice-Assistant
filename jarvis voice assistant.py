import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random

class JarvisAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        else:
            if voices:
                self.engine.setProperty('voice', voices[0].id)

        self.engine.setProperty('rate', 200)  # Faster speech
        self.engine.setProperty('volume', 0.9)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Fast ambient noise calibration
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Calibration complete. Ready for 'OK Jarvis'...")

        self.wake_phrases = ['ok jarvis', 'hey jarvis', 'jarvis']
        self.listening = True
        self.processing = False

    def speak(self, text):
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_wake_word(self):
        """Continuously listen for wake word (low latency and phrase_time_limit)."""
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=0.7, phrase_time_limit=2)
                try:
                    recognized = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {recognized}")
                    for wake in self.wake_phrases:
                        if wake in recognized:
                            print(f"Wake phrase: {wake}")
                            self.wake_up_response()
                            return True
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"API unavailable: {e}")
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Wake word error: {e}")
        return False

    def wake_up_response(self):
        if self.processing:
            return
        self.processing = True
        responses = [
            "Yes, how can I help you?",
            "I'm listening, what do you need?",
            "What can I do for you?",
            "How can I assist you today?"
        ]
        self.speak(random.choice(responses))
        command = self.listen_for_command()
        if command:
            self.process_command(command)
        else:
            self.speak("I didn't catch that. Try saying 'OK Jarvis' again.")
        self.processing = False

    def listen_for_command(self):
        """Listen for user command - faster limits, offline optional."""
        try:
            with self.microphone as source:
                print("Listening for command...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            try:
                # By default, use Google (fastest/most accurate).
                command = self.recognizer.recognize_google(audio)
                # For offline, install pocketsphinx and uncomment below:
                # command = self.recognizer.recognize_sphinx(audio)
            except sr.UnknownValueError:
                print("Could not understand the command")
                return None
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return None
            print(f"Command: {command.lower()}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("No command received")
            return None

    def process_command(self, command):
        print(f"Processing command: {command}")
        try:
            if 'wikipedia' in command:
                self.search_wikipedia(command)
            elif 'open youtube' in command:
                self.speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
            elif 'open google' in command:
                self.speak("Opening Google")
                webbrowser.open("https://google.com")
            elif 'open gmail' in command:
                self.speak("Opening Stack Overflow")
                webbrowser.open("https://gmail.com")
            elif 'open leetcode' in command:
                self.speak("opening leetcode")
                webbrowser.open("https://leetcode.com")
            elif 'open codechef' in command:
                self.speak("Opening CodeChef")
                webbrowser.open("https://codechef.com")
            elif 'open hive primary' in command:
                self.speak("Opening Hive Primary")
                webbrowser.open("https://hiveprimary.com")
            elif 'open udemy' in command:
                self.speak("Opening Udemy")
                webbrowser.open("https://udemy.com")
            elif 'open github' in command:
                self.speak("Opening GitHub")
                webbrowser.open("https://github.com")
            elif 'open linkedln' in command:
                self.speak("Opening LinkedIn")
                webbrowser.open("https://linkedin.com")
            elif 'open discord' in command:
                self.speak("Opening Discord")
                webbrowser.open("https://discord.com")
                
            elif any(phrase in command for phrase in ['what time', 'current time', 'time is it']):
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                self.speak(f"The current time is {current_time}")
            elif any(phrase in command for phrase in ['what date', 'current date', 'date today']):
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                self.speak(f"Today is {current_date}")
            elif 'weather' in command:
                self.speak("I do not have access to live weather data, try checking Google or a weather app.")
            elif any(phrase in command for phrase in ['hello', 'hi there', 'hey']):
                self.speak("Hello! How can I help you today?")
            elif 'how are you' in command:
                self.speak("I'm doing great! Thanks for asking. How can I assist you?")
            elif any(phrase in command for phrase in ['thank you', 'thanks']):
                self.speak("You're welcome! Is there anything else I can help you with?")
            elif 'joke' in command:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the scarecrow win an award? He was outstanding in his field!",
                    "Why don't eggs tell jokes? They'd crack each other up!",
                    "What do you call a fake noodle? An impasta!",
                    "Why did the math book look so sad? Because it was full of problems!"
                ]
                self.speak(random.choice(jokes))
            elif 'open notepad' in command:
                self.speak("Opening Notepad")
                os.system("notepad")
            elif 'open calculator' in command:
                self.speak("Opening Calculator")
                os.system("calc")
            elif any(phrase in command for phrase in ['stop listening', 'goodbye', 'exit', 'quit']):
                self.speak("Goodbye! Have a great day!")
                self.listening = False
            elif 'stop' in command:
                self.speak("Okay, I'll stop listening. Say 'OK Jarvis' to wake me up again.")
            else:
                self.speak("Sorry, I didn't get that. Try commands like Wikipedia search, open websites, time, or a joke.")
        except Exception as e:
            print(f"Error in command: {e}")
            self.speak("Sorry, I encountered an error processing that command.")

    def search_wikipedia(self, command):
        try:
            self.speak("Searching Wikipedia...")
            search_term = command.replace('wikipedia', '').replace('search', '').strip()
            if not search_term:
                self.speak("What should I search for on Wikipedia?")
                return
            summary = wikipedia.summary(search_term, sentences=2)
            self.speak(f"According to Wikipedia: {summary}")
        except wikipedia.exceptions.DisambiguationError:
            self.speak(f"I found multiple results for {search_term}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            self.speak(f"Sorry, I couldn't find any Wikipedia page for {search_term}")
        except Exception as e:
            print(f"Wikipedia error: {e}")
            self.speak("Sorry, I am having trouble accessing Wikipedia right now.")

    def start(self):
        self.speak("Jarvis is now active. Say 'OK Jarvis' to get my attention.")
        try:
            while self.listening:
                self.listen_for_wake_word()
        except KeyboardInterrupt:
            print("\nShutting down Jarvis...")
            self.speak("Jarvis is shutting down. Goodbye!")
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.speak("I encountered an unexpected error. Shutting down.")

def main():
    print("Initializing Jarvis Voice Assistant...")
    print("=" * 50)
    try:
        jarvis = JarvisAssistant()
        jarvis.start()
    except Exception as e:
        print(f"Failed to initialize Jarvis: {e}")
        print("Make sure all required packages are installed.")

if __name__ == "__main__":
    main()
