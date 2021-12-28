from pygame.image import load
from pygame.transform import rotate, scale
from pygame import Surface
from math import pi


class GameObject:
    x: float
    y: float
    yaw: float
    image_asset = None

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.yaw = .0

    def load_asset(self, path: str, _scale: tuple) -> None:
        self.image_asset = scale(load(path), _scale)

    def render(self, screen: Surface) -> None:
        rotated_image = rotate(self.image_asset, -self.yaw * 180 / pi)
        new_rect = rotated_image.get_rect(center=self.image_asset.get_rect(
            topleft=(round(self.x), round(self.y))).center)
        new_rect.center = (round(self.x), round(self.y))
        screen.blit(rotated_image, new_rect.topleft)
