from game.bullet import BulletArray
import pygame
from pygame.locals import *
from game.consts import *
from game.spaceship import MainShip, EnemyShip, SupportSatellite
from game.gui import GUI
from game.chat import Chat



class Game:
    main_ship: MainShip
    enemies: list[EnemyShip]
    enemy_bullets = BulletArray()

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.playarea = pygame.Surface((PLAYAREA_WIDTH, WINDOW_SIZE[1]))
        self.messagearea = pygame.Surface((MESSAGE_AREA_WIDTH, WINDOW_SIZE[1]))
        self.screen.fill((0, 0, 0))
        myfont = pygame.font.Font('assets/arcade.ttf', 30)
        self.finished = False
        self.gameover = False

        def render_text(text, font, colour, x, y, screen, allowed_width):
            words = text.split('\n')

            lines = []
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
                tx = x - fw / 2
                ty = y + y_offset

                font_surface = font.render(line, True, colour)
                screen.blit(font_surface, (tx, ty))
                y_offset += fh

        render_text(WELCOME_TEXT, myfont, (255, 255, 255), WINDOW_SIZE[0] / 2, 30, self.screen, WINDOW_SIZE[0] * 0.5)

        pygame.display.set_caption('Space Talkers')
        self.satellite = SupportSatellite()
        self.satellite.load_asset('assets/satellite.png', SS_SCALE)
        self.main_ship = MainShip()
        self.main_ship.load_asset('assets/ms.png', MS_SCALE)
        pygame.display.set_icon(self.main_ship.image_asset)
        self.chat = Chat()
        self.audio_busy = False

        stop = False

        while not stop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop = True
                    self.gameover = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stop = True
            self.clock.tick(FPS)
            pygame.display.flip()

        self.gui = GUI()
        self.enemies = []
        self.background = pygame.transform.scale(
            pygame.image.load('assets/bg.png'), WINDOW_SIZE)

    def recognize(self):
        pass

    def logic(self):
        bg_rect = self.background.get_rect(
            center=(PLAYAREA_WIDTH // 2, WINDOW_SIZE[1] // 2))
        self.playarea.blit(self.background, bg_rect)
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.gameover = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    if not self.gui.recording and not self.audio_busy:
                        self.recognize()
                        self.gui.start_recording()
                        self.audio_busy = True

        pressed_keys = pygame.key.get_pressed()
        self.main_ship.target_velocity = 0

        if not self.finished:
            if pressed_keys[pygame.K_d]:
                self.main_ship.set_yaw(MS_YAW_VELOCITY * S_PER_FRAME)

            if pressed_keys[pygame.K_a]:
                self.main_ship.set_yaw(-MS_YAW_VELOCITY * S_PER_FRAME)

            if (not pressed_keys[pygame.K_d]) and (not pressed_keys[pygame.K_a]) and pressed_keys[pygame.K_w]:
                self.main_ship.target_velocity = MS_SPEED

            if pressed_keys[pygame.K_SPACE]:
                self.main_ship.shoot()

        if len(self.enemies) < 3:
            enemy = EnemyShip()
            enemy.load_asset('assets/es.png', ES_SCALE)
            self.enemies.append(enemy)

        removed = 1
        for i in range(0, len(self.enemy_bullets._array)):
            if self.enemy_bullets._array[i - removed].move(S_PER_FRAME):
                self.enemy_bullets.remove_bullet(i - removed)
                removed += 1

        for i in range(0, len(self.enemy_bullets._array)):
            if self.main_ship.check_collision(self.enemy_bullets):
                if self.main_ship.deal_damage(ES_DAMAGE):
                    if not self.finished:
                        self.finished = True
                        self.chat.add_message({'from': 'game', 'message': 'Вы умерли. Но по крайней мере можете общаться со спутником'})

        for i in range(0, len(self.enemy_bullets._array)):
            self.enemy_bullets._array[i].render(self.playarea)

        self.main_ship.move(S_PER_FRAME)
        self.satellite.move(S_PER_FRAME, self.main_ship)

        for enemy in self.enemies:
            bullet = enemy.logic(self.main_ship, S_PER_FRAME)
            if bullet != None:
                self.enemy_bullets.add_bullet(bullet)
            enemy.move(S_PER_FRAME)

        removed = 0
        for i in range(0, len(self.enemies)):
            if self.enemies[i - removed].check_collision(self.main_ship.bullet_array):
                self.enemies.pop(i - removed)
                removed += 1

        for enemy in self.enemies:
            enemy.render(self.playarea)
        self.main_ship.render(self.playarea)
        self.satellite.render(self.playarea)

        self.gui.render(self.playarea, self)
        self.chat.render(self.messagearea)

        self.screen.blit(self.playarea, (0, 0))
        self.screen.blit(self.messagearea, (PLAYAREA_WIDTH, 0))
        pygame.display.flip()
        return self.gameover
