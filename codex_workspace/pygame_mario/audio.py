from pathlib import Path

import pygame


class SoundManager:
    def __init__(self, jump_path: str, coin_path: str, death_path: str) -> None:
        self.enabled = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            # No audio device or mixer init failed; keep game running silently.
            self.enabled = False

        self.jump_sound = self._load_sound(jump_path)
        self.coin_sound = self._load_sound(coin_path)
        self.death_sound = self._load_sound(death_path)

    def _load_sound(self, path: str) -> pygame.mixer.Sound | None:
        if not self.enabled or not path:
            return None
        file_path = Path(path)
        if not file_path.exists():
            return None
        try:
            return pygame.mixer.Sound(str(file_path))
        except pygame.error:
            return None

    @staticmethod
    def _play(sound: pygame.mixer.Sound | None) -> None:
        if sound is None:
            return
        sound.play()

    def play_jump(self) -> None:
        self._play(self.jump_sound)

    def play_coin(self) -> None:
        self._play(self.coin_sound)

    def play_death(self) -> None:
        self._play(self.death_sound)
