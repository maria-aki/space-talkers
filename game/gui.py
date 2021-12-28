from game.consts import *
from pygame import Surface, draw, image, Surface
from pygame.transform import scale
from pygame.time import get_ticks


class GUI:
    skill_icon_paths = ['assets/skill-icons/heal.png',
                        'assets/skill-icons/boost.png', 'assets/skill-icons/bomb.png']
    dark_skill_icon_paths = ['assets/skill-icons/heal-dark.png',
                             'assets/skill-icons/boost-dark.png', 'assets/skill-icons/bomb-dark.png']

    skill_icons: list[Surface]
    dark_skill_icons: list[Surface]

    microphone: Surface
    recording = False
    recording_time = 0

    def __init__(self) -> None:
        self.skill_icons = []
        self.dark_skill_icons = []
    
        for path in self.skill_icon_paths:
            self.skill_icons.append(scale(image.load(path), ICON_SIZE))
        for path in self.dark_skill_icon_paths:
            self.dark_skill_icons.append(scale(image.load(path), ICON_SIZE))

        self.microphone = scale(image.load('assets/micro.png'), ICON_SIZE)

    def start_recording(self):
        self.recording = True

    def render(self, screen: Surface, game) -> None:
        draw.rect(screen, (222, 22, 76),
                  (0, WINDOW_SIZE[1] - HP_BAR_HEIGHT, PLAYAREA_WIDTH, WINDOW_SIZE[1]))
        draw.rect(screen, (13, 222, 72), (0,
                  WINDOW_SIZE[1] - HP_BAR_HEIGHT, game.main_ship.hp * PLAYAREA_WIDTH // MS_MAX_HP, WINDOW_SIZE[1]))

        for icon, i in zip(self.dark_skill_icons, range(0, len(self.dark_skill_icons))):
            screen.blit(icon, (i * ICON_SIZE[0], WINDOW_SIZE[1] - ICON_SIZE[1] - HP_BAR_HEIGHT))
        for icon, i in zip(self.skill_icons, range(0, len(self.skill_icons))):
            part = min((get_ticks() - game.satellite.last_time_used[i]) / game.satellite.cooldowns[i], 1)
            new_icon = icon.subsurface((0, ICON_SIZE[1] - part * ICON_SIZE[1], ICON_SIZE[0], part * ICON_SIZE[1]))
            screen.blit(new_icon, (i * ICON_SIZE[0], WINDOW_SIZE[1] - ICON_SIZE[1] - HP_BAR_HEIGHT + (ICON_SIZE[1] - part * ICON_SIZE[1])))
        
        if self.recording:
            screen.blit(self.microphone, (len(self.skill_icons) * ICON_SIZE[0], WINDOW_SIZE[1] - ICON_SIZE[1] - HP_BAR_HEIGHT))