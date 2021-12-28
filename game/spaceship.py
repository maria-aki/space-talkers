from pygame.time import get_ticks
from pygame import Surface
from game.bullet import BulletArray
from game.game_object import GameObject
from game.bullet import Bullet, BulletArray
from game.consts import *
from math import sin, cos, pi, atan2
from random import randint


class SpaceShip(GameObject):
    bullet_array: BulletArray
    vx, vy = 0, 0
    target_velocity = 0
    accel, friction = 0, 0
    dx, dy = 0, 0
    prev_yaw = 0
    bullet_asset: str
    last_shot_time = 0
    bullet_delay = 200
    size = (20, 20)

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.yaw = 0
        self.bullet_array = BulletArray()

    def shoot(self) -> None:
        if get_ticks() - self.last_shot_time >= self.bullet_delay:
            bullet = Bullet(self.x + self.size[0] * cos(self.yaw) / 3,
                            self.y + self.size[1] * sin(self.yaw) / 3, self.yaw)
            bullet.max_distance = 1000
            bullet.load_asset(self.bullet_asset, (25, 25))
            self.bullet_array.add_bullet(bullet)
            self.last_shot_time = get_ticks()

    def set_yaw(self, dyaw: float) -> None:
        self.yaw += dyaw
        if self.yaw > pi:
            self.yaw -= 2 * pi
        if self.yaw < -pi:
            self.yaw += 2 * pi
        if self.target_velocity != 0:
            self.prev_yaw = self.yaw

    def move(self, dt: float) -> None:
        if self.target_velocity > 0:
            if self.target_velocity * cos(self.yaw) > 0:
                self.vx = min(self.vx + dt * self.accel * cos(self.yaw),
                              self.target_velocity * cos(self.yaw))
            else:
                self.vx = max(self.vx + dt * self.accel * cos(self.yaw),
                              self.target_velocity * cos(self.yaw))

            if self.target_velocity * sin(self.yaw) > 0:
                self.vy = min(self.vy + dt * self.accel * sin(self.yaw),
                              self.target_velocity * sin(self.yaw))
            else:
                self.vy = max(self.vy + dt * self.accel * sin(self.yaw),
                              self.target_velocity * sin(self.yaw))
        else:
            if self.vx > 0:
                self.vx = max(
                    self.vx - abs(dt * self.friction * cos(self.prev_yaw)), 0)
            else:
                self.vx = min(
                    self.vx + abs(dt * self.friction * cos(self.prev_yaw)), 0)

            if self.vy > 0:
                self.vy = max(
                    self.vy - abs(dt * self.friction * sin(self.prev_yaw)), 0)
            else:
                self.vy = min(
                    self.vy + abs(dt * self.friction * sin(self.prev_yaw)), 0)

        self.x += self.vx * dt
        self.y += self.vy * dt

        removed = 0
        for i in range(0, len(self.bullet_array._array)):
            if self.bullet_array._array[i - removed].move(dt):
                self.bullet_array.remove_bullet(i)
                removed += 1

    def render(self, screen: Surface) -> None:
        for bullet in self.bullet_array._array:
            bullet.render(screen)
        super().render(screen)

    def check_collision(self, bullet_array: BulletArray) -> None:
        for i in range(0, len(bullet_array._array)):
            if (self.x - bullet_array._array[i].x) ** 2 + (self.y - bullet_array._array[i].y) ** 2 <= (self.size[0] / 2) ** 2:
                bullet_array.remove_bullet(i)
                return True
        return False


class MainShip(SpaceShip):
    hp = MS_MAX_HP
    boosted = False
    boost_time: int

    def __init__(self) -> None:
        super().__init__(PLAYAREA_WIDTH / 2, WINDOW_SIZE[1] / 2)
        self.velocity = 0
        self.accel = MS_ACCEL
        self.friction = MS_FRICTION
        self.size = MS_SCALE
        self.bullet_asset = 'assets/ms_bullet.png'

    def move(self, dt: float) -> None:
        if self.boosted:
            if get_ticks() - self.boost_time >= MS_BOOST_DURATION:
                self.boosted = False
        if self.boosted:
            self.accel *= MS_BOOST_RATE
            self.target_velocity *= MS_BOOST_RATE

        prev_x = self.x
        prev_y = self.y
        super().move(dt)
        if self.x < GAP:
            self.x = prev_x
            self.vx = -self.vx
        elif self.x > PLAYAREA_WIDTH - GAP:
            self.x = prev_x
            self.vx = -self.vx
        if self.y < GAP:
            self.y = prev_y
            self.vy = -self.vy
        elif self.y > WINDOW_SIZE[1] - GAP:
            self.y = prev_y
            self.vy = -self.vy

        if self.boosted:
            self.accel /= MS_BOOST_RATE
            self.target_velocity /= MS_BOOST_RATE

    def deal_damage(self, damage: int) -> bool:
        self.hp = max(0, self.hp - damage)
        return self.hp == 0

    def boost(self) -> None:
        self.boosted = True
        self.boost_time = get_ticks()


class EnemyShip(SpaceShip):
    def __init__(self) -> None:
        self.accel = ES_ACCEL
        self.friction = ES_FRICTION
        self.size = ES_SCALE

        if randint(0, 1):
            x = randint(-GAP, PLAYAREA_WIDTH + GAP)
            if randint(0, 1):
                y = -GAP
            else:
                y = WINDOW_SIZE[1] + GAP
        else:
            y = randint(-GAP, WINDOW_SIZE[1] + GAP)
            if randint(0, 1):
                x = -GAP
            else:
                x = PLAYAREA_WIDTH + GAP
        self.yaw = randint(-31415, 31415) / 10000

        super().__init__(x, y)
        self.velocity = 0
        self.accel = ES_ACCEL
        self.friction = ES_FRICTION
        self.size = ES_SCALE
        self.bullet_asset = 'assets/es_bullet.png'
        self.bullet_delay = 1000

    def shoot(self) -> Bullet:
        if get_ticks() - self.last_shot_time >= self.bullet_delay:
            bullet = Bullet(self.x + self.size[0] * cos(self.yaw) / 3,
                            self.y + self.size[1] * sin(self.yaw) / 3, self.yaw)
            bullet.load_asset(self.bullet_asset, (25, 25))
            self.last_shot_time = get_ticks()
            return bullet
        return None

    def logic(self, main_ship: MainShip, dt: float) -> None or Bullet:
        bullet = None
        angle = atan2(self.y - main_ship.y, self.x - main_ship.x) + pi
        if angle > pi:
            angle -= 2 * pi
        if angle < -pi:
            angle += 2 * pi

        if angle - VIEW_RANGE < self.yaw < angle + VIEW_RANGE:
            self.target_velocity = ES_SPEED
            if angle - SHOOT_RANGE < self.yaw < angle + SHOOT_RANGE:
                bullet = self.shoot()
                if (self.x - main_ship.x) ** 2 + (self.y - main_ship.y) ** 2 <= 300 ** 2:
                    self.target_velocity = 0
        else:
            self.target_velocity = 0

        if angle > self.yaw:
            if angle - self.yaw < pi:
                self.set_yaw(ES_YAW_VELOCITY * dt)
            else:
                self.set_yaw(-ES_YAW_VELOCITY * dt)
        else:
            if self.yaw - angle < pi:
                self.set_yaw(-ES_YAW_VELOCITY * dt)
            else:
                self.set_yaw(ES_YAW_VELOCITY * dt)

        return bullet


class SupportSatellite(GameObject):
    radius = 100
    cooldowns = [15000, 10000, 20000]
    last_time_used = [0, 0, 0]

    def __init__(self) -> None:
        super().__init__(0.0, 0.0)
        for i in range(0, len(self.last_time_used)):
            self.last_time_used[i] = get_ticks()

        def heal(game) -> None:
            game.main_ship.hp = min(
                game.main_ship.hp + SS_HEAL_VALUE, MS_MAX_HP)

        def boost(game) -> None:
            game.main_ship.boost()

        def kill_all(game) -> None:
            game.enemies = []

        self.skills = [heal, boost, kill_all]

    def move(self, dt: float, main_ship: MainShip) -> None:
        self.yaw += dt * SS_YAW_VELOCITY
        self.x = main_ship.x + self.radius * cos(self.yaw + pi)
        self.y = main_ship.y + self.radius * sin(self.yaw + pi)

    def use_skill(self, skill_id: int, game) -> bool:
        if skill_id in range(0, len(self.last_time_used)):
            if get_ticks() - self.last_time_used[skill_id] >= self.cooldowns[skill_id]:
                self.skills[skill_id](game)
                self.last_time_used[skill_id] = get_ticks()
                return True
        return False
