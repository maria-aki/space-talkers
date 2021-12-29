import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self) -> None:
        self.r = sr.Recognizer()

    def recognize(self) -> str:
        with sr.Microphone() as source:
            # print("Слушаю")
            audio = self.r.listen(source)
        
        try:
            line = self.r.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            line = ''
        return line
