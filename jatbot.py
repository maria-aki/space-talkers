from requests import get
from random import choice
from game.consts import *
import pymorphy2


class JatBot:
    def __init__(self) -> None:
        pass

    def ask(self, text: str) -> str:
        try:
            r = get(JATBOT_LINK, params={'text': text})
            if r.status_code == 200:
                return r.text
            else:
                return 'сервер с ботом упал'
        except:
            return 'сервер с ботом упал'


class SkillChecker:
    # Ответы если навык перезаряжается
    cd_response = ['Перезарядка.', 'Слишком рано.', 'Придется подождать.']
    # Названия навыков
    skill_names = ['лечение', 'ускорение', 'взрыв']
    # Слова призывающие к действию
    action_words = ['использовать', 'применить']
    # Как можно назвать навык
    action_name_words = ['навык', 'способность', 'умение']

    # Ответы боты
    skill_responses = [
        ['Щиты восстановлены.', 'Чиню корабль.'],
        ['Скорость увеличена.', 'Ускоряю.'],
        ['Сбрасываю бомбу.', 'Взрываю.']
    ]

    # Игнорируемые слова
    ignorables = ['пожалуйста', 'же', 'срочно', 'сейчас', 'прошу']

    # Шаблоны
    templates = [
        ['skill_word'],
        ['action_word', 'skill_word'],
        ['action_word', 'action_name_word', 'skill_word'],
        ['action_name_word', 'skill_word']
    ]

    def __init__(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer(path='assets/dict')

    def ask(self, _text: str) -> dict:
        text = _text.split()

        # Удалим ненужные для нас слова (причем по одному разу, если их больше одного то уже странно)
        for ignorable in self.ignorables:
            if ignorable in text:
                text.pop(text.index(ignorable))

        # Составляем шаблон
        template = []
        normalized_text = [self.morph.parse(
            word)[0].normal_form for word in text]
        for word in normalized_text:
            if word in self.skill_names:
                template.append('skill_word')
            elif word in self.action_words:
                template.append('action_word')
            elif word in self.action_name_words:
                template.append('action_name_word')
        # Проверим все ли слова подошли по шаблону
        if len(template) != len(text):
            return {'ok': False}

        # Ищем совпадение по шаблону
        for temp in self.templates:
            if template == temp:
                skill_index = self.skill_names.index(
                    list(set(normalized_text) & set(self.skill_names))[0])
                return {'ok': True, 'id': skill_index, 'response': choice(self.skill_responses[skill_index])}
        return {'ok': False}

    def get_cooldown_message(self) -> str:
        return choice(self.cd_response)
