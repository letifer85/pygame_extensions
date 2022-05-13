from __future__ import annotations

import re
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from typing import Sequence, Callable, Mapping


class AnimationLoopType(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    ISOLATING = 'isolating'
    REPEATING = 'repeating'
    REPEATING_BACKWARD = 'repeating_backward'

    _ignore_: str | list[str] = ['__REVERSE_MAP__']
    __REVERSE_MAP__: Mapping[AnimationLoopType, AnimationLoopType]

    def reverse(self) -> AnimationLoopType:
        return AnimationLoopType.__REVERSE_MAP__[self]


AnimationLoopType.__REVERSE_MAP__ = {
    AnimationLoopType.FORWARD: AnimationLoopType.BACKWARD,
    AnimationLoopType.BACKWARD: AnimationLoopType.FORWARD,
    AnimationLoopType.ISOLATING: AnimationLoopType.ISOLATING,
    AnimationLoopType.REPEATING: AnimationLoopType.REPEATING_BACKWARD,
    AnimationLoopType.REPEATING_BACKWARD: AnimationLoopType.REPEATING
}


class Animation(pygame.Surface):

    ORIGIN_POINT = pygame.Vector2(0, 0)
    ALLOWED_EXTENSION = {'.png'}
    DEFAULT_ANIMATION_TIME = 1000

    def __init__(
        self,
        surfaces: Sequence[pygame.surface.Surface],
        size: pygame.Vector2,
        scale: float,
        animation_time: int,
        tag: str,
        callback: Callable[[str], None],
        loop_type: AnimationLoopType,
    ):
        if not surfaces:
            raise ValueError('`Animation.surfaces` is ether None or an empty Sequence')

        surfaces = [
            pygame.transform.scale(
                surface, pygame.Vector2(size) * scale
            ) for surface in surfaces
        ]

        super().__init__(surfaces[0].get_size())

        self.surfaces = surfaces
        self.index = 0
        self.flip_interval = int(animation_time / len(self.surfaces))
        self.tag = tag
        self.callback = callback
        self.loop_type = loop_type
        self.playing = False
        self.time_since_flip = 0
        self.surfaces_count = len(self.surfaces)
        if self.loop_type in (
            AnimationLoopType.BACKWARD,
            AnimationLoopType.REPEATING_BACKWARD,
        ):
            self.surfaces = list(reversed(self.surfaces))
            self.reversed = True
        else:
            self.reversed = False
        self.current_image = self.surfaces[self.index]
        self.blit(self.current_image, Animation.ORIGIN_POINT)

    @classmethod
    def from_folder_path(
        cls,
        folder_path: str,
        size: pygame.Vector2 | None = None,
        scale: float = 1,
        animation_time: int = DEFAULT_ANIMATION_TIME,
        tag: str = 'Animation',
        callback: Callable[[str], None] = lambda x: None,
        loop_type: AnimationLoopType = AnimationLoopType.FORWARD,
    ) -> Animation:
        surfaces = [
            pygame.image.load(image_path)
            for image_path in sorted(
                Path(folder_path).glob(r'*.*'),
                key=lambda key: [
                    (lambda text: int(text) if text.isdigit() else text)(c)
                    for c in re.split('([0-9]+)', str(key))
                ],
            )
            if image_path.suffix in cls.ALLOWED_EXTENSION
        ]
        size = size or pygame.Vector2(surfaces[0].get_size())
        return cls(surfaces, size, scale, animation_time, tag, callback, loop_type)

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(self.current_image.get_size())

    def flip_image(self) -> None:
        match self.loop_type:
            case AnimationLoopType.FORWARD | AnimationLoopType.BACKWARD:
                self.index += 1
            case AnimationLoopType.REPEATING | AnimationLoopType.REPEATING_BACKWARD:
                self.index = (self.index + 1) % self.surfaces_count
            case AnimationLoopType.ISOLATING:
                if self.index == self.surfaces_count - 1:
                    self.reverse()
                self.index += 1

        if self.index not in range(self.surfaces_count):
            self.end()

        if self.playing:
            self.fill((0, 0, 0, 0))
            self.current_image = self.surfaces[self.index]
            self.blit(self.current_image, Animation.ORIGIN_POINT)

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def end(self):
        self.stop()
        self.callback(self.tag)

    def reverse(self):
        self.surfaces = list(reversed(self.surfaces))
        self.index = self.surfaces_count - self.index
        self.reversed = not self.reversed
        self.loop_type = self.loop_type.reverse()

    def reset(self):
        self.stop()
        self.surfaces = list(reversed(self.surfaces)
                             if self.reversed else self.surfaces)
        self.index = 0

    def update(self, delta_time: int) -> None:
        if not self.playing:
            return
        self.time_since_flip += delta_time
        if self.time_since_flip >= self.flip_interval:
            self.time_since_flip -= self.flip_interval
            self.flip_image()
