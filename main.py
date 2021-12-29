from talker import TTS
from jatbot import JatBot, SkillChecker
import threading
from audio import SpeechRecognizer
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from game.game import Game


if __name__ == '__main__':
    game = Game()
    jatbot = JatBot()
    skillchecker = SkillChecker()
    recognizer = SpeechRecognizer()
    tts = TTS()

    def record_and_recognize() -> None:
        line = recognizer.recognize().lower()
        game.gui.recording = False
        # print('Вы сказали:', line)
        game.chat.add_message({'from': 'mc', 'message': line})
        skill_to_use = None

        result = skillchecker.ask(line.lower())

        if result['ok']:
            skill_to_use = result['id']
            phrase = result['response']
        else:
            phrase = jatbot.ask(line)

        if skill_to_use is not None:
            if game.finished:
                phrase = 'Нельзя использовать способности. Мы проиграли'
            elif not game.satellite.use_skill(skill_to_use, game):
                phrase = skillchecker.get_cooldown_message()

        # print('Бот ответил:', phrase)
        game.chat.add_message({'from': 'satellite', 'message': phrase.lower()})
        if phrase != '':
            tts.say(phrase)
        game.audio_busy = False

    thread = threading.Thread(target=record_and_recognize)

    def launch_thread() -> None:
        global thread
        if not thread.is_alive():
            thread = threading.Thread(target=record_and_recognize)
            thread.start()

    game.recognize = launch_thread

    while True:
        if game.logic():
            break
