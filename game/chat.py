from pygame import Surface, font, draw
from game.consts import *


def render_text(payload, text, font, colour, x, y, screen, allowed_width):
    words = text.split()

    lines = [payload]
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)
        tx = x
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))
        y_offset += fh

    return y_offset


class Chat:
    messages: list[dict]

    def __init__(self) -> None:
        self.messages = []
        self.font_size = 18
        self.font = font.Font('assets/arcade.ttf', self.font_size)

    def add_message(self, message: dict) -> None:
        self.messages.append(message)

    def render(self, screen: Surface) -> None:
        screen.fill((212, 39, 227))

        gap = 20
        offset = -gap
        x_offset = 10
        for message in self.messages[::-1]:
            if message['from'] == 'mc':
                payload = 'Вы сказали:'
                bg_color = (250, 54, 181)
            elif message['from'] == 'game':
                payload = 'Важная информация:'
                bg_color = (129, 121, 246)    
            else:
                payload = 'Спутник ответил:'
                bg_color = (178, 43, 253)

            height = render_text(payload, message['message'], self.font,
                                 (255, 255, 255), x_offset, offset + gap, screen, MESSAGE_AREA_WIDTH - x_offset)

            draw.rect(screen, bg_color, (0, offset + gap, MESSAGE_AREA_WIDTH, gap + height))
            render_text(payload, message['message'], self.font,
                        (255, 255, 255), x_offset, int(offset + gap * 1.4), screen, MESSAGE_AREA_WIDTH - x_offset)

            offset += height + gap

        if offset > WINDOW_SIZE[1] * 2:
            self.messages.pop(0)
