#Erin Corteville, Taylor Scott
#Novermber 3, 2018
#VandyHacks V

#This file contains the main function for CadenzaKeysself.

from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings

def main():
    # parse command line arguments
    (args, parser) = parse_arguments()

    # enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    fps, sound = wavfile.read(args.wav.name)

    tones = range(-25, 25)
    sys.stdout.write('Transponding sound file...')
    sys.stdout.flush()
    transposed_sounds = [pitchshift(sound, n) for n in tones]
    print('DONE')

    #?
    pygame.mixer.init(fps, -16, 1, 2048)
    # for the focus
    screen = pygame.display.set_mode((150,150))

    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    is_playing = {k: False for k in keys}

    while true:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # stops with 50ms fadeout
            key_sound[key].fadeout(50)
            is_playing[key] = False

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('See ya later Alligator')
