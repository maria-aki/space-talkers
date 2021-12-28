import pyttsx3

class TTS:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()

    def say(self, text) -> None:
        self.engine.say(text)
        self.engine.runAndWait()