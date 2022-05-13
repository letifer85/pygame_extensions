from __future__ import annotations
from cmath import sin
import math

import pygame

from pygame_extensions import Animation, AnimationLoopType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Literal

class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(
        self, 
        animation_folder_path: str,
        position: pygame.Vector2,
        placement: Literal["topleft", "topright", "bottomleft", "bottomright", "center"] = "center",
        size: pygame.Vector2 | None = None,
        scale: float = 1,
        animation_time: int = Animation.DEFAULT_ANIMATION_TIME,
        animation_tag: str = 'Animation',
        animation_callback: Callable[[str], None] = lambda x: None,
        animation_loop_type: AnimationLoopType = AnimationLoopType.FORWARD,
        groups: pygame.sprite.AbstractGroup = (),
    ) -> None:
        super().__init__(groups)
        self.animation = Animation.from_folder_path(
            animation_folder_path,
            size,
            scale,
            animation_time,
            animation_tag,
            animation_callback,
            animation_loop_type
        )
        self.position = position
        self.placement = placement
        self.size = self.animation.size
        self.image = self.animation.current_image
        self.rect = self.animation.get_rect(**{self.placement: self.position})

    offset = 0
    speed = 0.05
    sin_scale = 100
    def update(self, delta_time: int) -> None:
        self.animation.update(delta_time)
        self.image = self.animation.current_image
        position = self.position.copy()
        position.x += int(math.sin(AnimatedSprite.offset) * AnimatedSprite.sin_scale)
        position.y += int(math.cos(AnimatedSprite.offset) * AnimatedSprite.sin_scale)
        self.rect = self.animation.get_rect(**{self.placement: self.position})
        AnimatedSprite.offset += AnimatedSprite.speed
        

if __name__ == '__main__':
    pygame.init()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    explosion_group = pygame.sprite.GroupSingle()
    explosion = AnimatedSprite(
        animation_folder_path= 'test_assets\PNG\Explosion_blue_circle',
        position = pygame.Vector2(250, 250),
        placement = "center",
        size = None,
        scale = 1,
        animation_time  = Animation.DEFAULT_ANIMATION_TIME,
        animation_tag = 'SpriteAnimation',
        animation_callback = lambda x: explosion.kill(),
        animation_loop_type = AnimationLoopType.REPEATING,
        groups=(explosion_group,)
    )
    explosion.animation.play()
    clock = pygame.time.Clock()
    running = True
    while running:
        delta_time = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        explosion_group.update(delta_time)
        screen.fill('black')
        explosion_group.draw(screen)
        pygame.display.flip()
