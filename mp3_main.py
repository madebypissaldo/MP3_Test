import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))

WHITE = (255,255,255)
BLACK = (0,0,0)

font = pygame.font.SysFont('Arial', 24)

menu = True
music_menu = False
genero = ''
musica = ''
music_file = ''

def draw_menu():
    screen.fill(WHITE)
    text = font.render('Selecione o genero musical:', True, BLACK)
    screen.blit(text, (100, 100))
    text = font.render('1 - Drill', True, BLACK)
    screen.blit(text, (100, 150))
    text = font.render('2 - Corridos Tumbados', True, BLACK)
    screen.blit(text, (100, 200))
    text = font.render('3 - RnB', True, BLACK)
    screen.blit(text, (100, 250))
    text = font.render('Q - Sair', True, BLACK)
    screen.blit(text, (50, 50))
    pygame.display.update()

def draw_music_menu():
    screen.fill(WHITE)
    text = font.render('Selecione uma musica:', True, BLACK)
    screen.blit(text, (100, 100))
    if genero == '1':
        text = font.render('1 - Doja - Central Cee', True, BLACK)
        screen.blit(text,(100,200))
        text = font.render('2 - Irish Drill - AC-130', True, BLACK)
        screen.blit(text, (100, 250))
        text = font.render('utilize a tecla D para iniciar a musica e a tecla ESPAÇO para pausar', True, BLACK)
        screen.blit(text, (100, 300))
        text = font.render('Q - voltar', True, BLACK)
        screen.blit(text, (50, 50))
    elif genero == '2':
        text = font.render('3 - Bizarrap Session - Peso Pluma', True, BLACK)
        screen.blit(text, (100,200))
        text = font.render('4 - TQM - Fuerza Regida', True, BLACK)
        screen.blit(text, (100,250))
        text = font.render('utilize a tecla D para iniciar a musica e a tecla ESPAÇO para pausar', True, BLACK)
        screen.blit(text, (100, 300))
        text = font.render('Q - voltar', True, BLACK)
        screen.blit(text, (50, 50))
    elif genero == "3":
        text = font.render("5 - Ivy - Frank Ocean", True, BLACK)
        screen.blit(text, (100, 200))
        text = font.render("6 - After Hours - The Weeknd", True, BLACK)
        screen.blit(text, (100, 250))
        text = font.render('utilize a tecla D para iniciar a musica e a tecla ESPAÇO para pausar', True, BLACK)
        screen.blit(text, (100, 300))
        text = font.render('Q - voltar', True, BLACK)
        screen.blit(text, (50, 50))
    pygame.display.update()

def draw_pause_menu():
    screen.fill(WHITE)
    text = font.render("Música pausada", True, BLACK)
    screen.blit(text, (100, 100))
    text = font.render("Pressione espaço para continuar", True, BLACK)
    screen.blit(text, (100, 150))
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if menu:
                if event.key == pygame.K_1:
                    genero = "1"
                    menu = False
                    music_menu = True
                elif event.key == pygame.K_2:
                    genero = "2"
                    menu = False
                    music_menu = True
                elif event.key == pygame.K_3:
                    genero = "3"
                    menu = False
                    music_menu = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            elif music_menu:
                if event.key == pygame.K_1:
                    musica = "1"
                elif event.key == pygame.K_2:
                    musica = "2"
                elif event.key == pygame.K_3:
                    musica = "3"
                elif event.key == pygame.K_4:
                    musica = "4"
                elif event.key == pygame.K_5:
                    musica = "5"
                elif event.key == pygame.K_6:
                    musica = "6"
                elif event.key == pygame.K_SPACE:
                    if music_file:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                elif event.key == pygame.K_d:
                    if musica == "1":
                        music_file = "ytmp3-converter.com_320kbps-central-cee-doja-official-music-video.mp3"
                    elif musica == "2":
                        music_file = "ytmp3-converter.com_320kbps-irish-drill.mp3"
                    elif musica == "3":
                        music_file = "ytmp3-converter.com_320kbps-peso-pluma-bzrp-music-sessions-55.mp3"
                    elif musica == "4":
                        music_file = "ytmp3-converter.com_320kbps-fuerza-regida-tqm.mp3"
                    elif musica == "5":
                        music_file = "ytmp3-converter.com_320kbps-frank-ocean-ivy.mp3"
                    elif musica == "6":
                        music_file = "ytmp3-converter.com_320kbps-the-weeknd-after-hours-audio.mp3"
                        
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()
                elif event.key == pygame.K_q:
                    music_menu = False
                    menu = True

    if menu:
        draw_menu()
    elif music_menu:
        draw_music_menu()
    elif music_file:
        if pygame.mixer.music.get_busy():
            draw_pause_menu()


    pygame.display.update()
    pygame.time.Clock().tick(60)