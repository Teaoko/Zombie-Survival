import os
import sys
import pygame

_SOUND_CACHE: dict[tuple[str, float | None], pygame.mixer.Sound] = {}


def resource_path(relative_path: str) -> str:
    """Resolve resource paths for dev and PyInstaller bundles."""
    base_path = getattr(sys, "_MEIPASS", None) or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)


def sounds_dir() -> str:
    return os.path.normpath(resource_path("Sounds"))


def load_sound(filename: str, volume: float | None = None) -> pygame.mixer.Sound:
    key = (filename, volume)
    if key in _SOUND_CACHE:
        return _SOUND_CACHE[key]
    full_path = os.path.join(sounds_dir(), filename)
    snd = pygame.mixer.Sound(full_path)
    if volume is not None:
        snd.set_volume(volume)
    _SOUND_CACHE[key] = snd
    return snd


def preload_common_sounds() -> None:
    for name, vol in [
        ("Turret fired.wav", 0.5),
        ("Turret reload.wav", 0.5),
        ("Can't reload.wav", 0.5),
        ("Turret hit.wav", 0.5),
        ("Zombie hit.wav", 0.5),
        ("Game over.wav", 0.5),
    ]:
        try:
            load_sound(name, vol)
        except Exception:
            # Ignore missing optional assets
            pass
