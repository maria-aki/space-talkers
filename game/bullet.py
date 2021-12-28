from game.game_object import GameObject
from math import sin, cos, sqrt


class Bullet(GameObject):
    start_x: float
    start_y: float
    velocity = 500.0
    max_distance = 400.0

    def __init__(self, x: float, y: float, yaw: float) -> None:
        super().__init__(x, y)
        self.yaw = yaw
        self.dx = self.velocity * cos(self.yaw)
        self.dy = self.velocity * sin(self.yaw)
        self.start_x = x
        self.start_y = y

    def move(self, dt: float) -> bool:
        self.x += self.dx * dt
        self.y += self.dy * dt

        if sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2) >= self.max_distance:
            return True
        else:
            return False


class BulletArray:
    _array: list[Bullet]

    def __init__(self) -> None:
        self._array = []

    def add_bullet(self, bullet: Bullet) -> None:
        self._array.append(bullet)

    def remove_bullet(self, index: int) -> None:
        self._array.pop(index)

    def logic(self) -> None:
        for i in range(0, len(self._array)):
            if self._array[i].move():
                self.remove_bullet(i)
