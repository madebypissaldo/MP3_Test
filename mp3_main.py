import pygame
import sys

pygame.init()

while True:
    genero = input('qual genero musical você deseja ouvir? \n1 - drill\n2 - corridos\n3 - RnB\n4 - Sair\n ')
    if genero == "1":
        musica = input('qual musica você deseja ouvir?\nD1:  Doja - Central Cee \nD2: Irish Drill - AC-130\n ')
        if musica == 'd1'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-central-cee-doja-official-music-video.mp3'
        elif musica == 'd2'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-irish-drill.mp3'
        else:
            print('musica não encontrada')
            continue
    elif genero == '2':
        musica = input('qual musica você deseja ouvir?\nC1 : Bizarrap Session - Peso Pluma\n C2: TQM - Fuerza Regida\n')
        if musica == 'c1'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-peso-pluma-bzrp-music-sessions-55.mp3'
        elif musica == 'c2'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-fuerza-regida-tqm.mp3'
        else:
            print('musica não encontrada')
            continue
    elif genero == '3':
        musica = input('qual musica você deseja ouvir:\nR1: Ivy - Frank Ocean \nR2: After Hours  - The Weeknd \n')
        if musica == 'r1'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-frank-ocean-ivy.mp3'
        elif musica == 'r2'.strip().lower():
            music_file = 'ytmp3-converter.com_320kbps-the-weeknd-after-hours-audio.mp3'
        else:
            print('musica não encontrada')
            continue
    elif genero == '4':
        print('Saindo do programa...')
        pygame.quit()
        sys.exit()
    else:
        print('genero não encontrado')
        continue

    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

        replay = True
        while replay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                elif event.type == pygame.USEREVENT + 1:
                    replay = False
            pygame.time.Clock().tick(60)

        play_again = input('deseja ouvir outra musica? (s/n)\n')
        if play_again != 's'.strip().lower():
            break

    except pygame.error as e:
        print(f'erro ao carregar a musica: {e}')

pygame.quit()
sys.exit()