import numpy as np

import pygame
def generate_tone(frequency, duration=1.0, amplitude=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    # Convert to 16-bit integers
    sound_data = (wave * 32767).astype(np.int16)
    # Make it 2D for stereo and ensure it's C-contiguous
    sound_data = np.column_stack((sound_data, sound_data))
    # Ensure the array is C-contiguous
    sound_data = np.ascontiguousarray(sound_data)
    return pygame.sndarray.make_sound(sound_data)

