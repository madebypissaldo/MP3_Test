import pygame
import sys

pygame.init()

# Configurações da tela e cores
screen = pygame.display.set_mode((800, 600))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

font = pygame.font.SysFont('Arial', 24)

# Estados do menu
menu = True
music_menu = False
genero = ''
musica = ''
music_file = ''
volume = 1.0

# Gêneros e Músicas organizados em dicionários
generos = {
    '1': 'Drill',
    '2': 'Corrido Tumbado',
    '3': 'RnB'
}

musicas_por_genero = {
    '1': [('Doja - Central Cee', './ytmp3-converter.com_320kbps-central-cee-doja-official-music-video.mp3'),
          ('Irish Drill - AC-130', './ytmp3-converter.com_320kbps-irish-drill.mp3')],
    '2': [('Bizarrap Session - Peso Pluma', './ytmp3-converter.com_320kbps-peso-pluma-bzrp-music-sessions-55.mp3'),
          ('TQM - Fuerza Regida', './ytmp3-converter.com_320kbps-fuerza-regida-tqm.mp3')],
    '3': [('Ivy - Frank Ocean', './ytmp3-converter.com_320kbps-frank-ocean-ivy.mp3'),
          ('After Hours - The Weeknd', './ytmp3-converter.com_320kbps-the-weeknd-after-hours-audio.mp3')]
}

# Criando uma classe de botão
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


# Funções de ação para os botões
def select_genero_1():
    global genero, menu, music_menu
    genero = '1'
    menu = False
    music_menu = True

def select_genero_2():
    global genero, menu, music_menu
    genero = '2'
    menu = False
    music_menu = True

def select_genero_3():
    global genero, menu, music_menu
    genero = '3'
    menu = False
    music_menu = True

def quit_program():
    pygame.quit()
    sys.exit()

# Criando os botões do menu principal
buttons_menu = [
    Button("1 - Drill", 100, 150, 200, 50, GRAY, DARK_GRAY, select_genero_1),
    Button("2 - Corrido Tumbado", 100, 220, 200, 50, GRAY, DARK_GRAY, select_genero_2),
    Button("3 - RnB", 100, 290, 200, 50, GRAY, DARK_GRAY, select_genero_3),
    Button("Sair", 50, 50, 100, 50, GRAY, DARK_GRAY, quit_program)
]

def draw_menu():
    screen.fill(WHITE)
    text = font.render('Selecione o genero musical:', True, BLACK)
    screen.blit(text, (100, 100))
    for button in buttons_menu:
        button.draw(screen)
    pygame.display.update()

# Funções para música
def draw_music_menu():
    screen.fill(WHITE)
    text = font.render('Selecione uma musica:', True, BLACK)
    screen.blit(text, (100, 100))
    if genero in musicas_por_genero:
        for idx, (nome_musica, _) in enumerate(musicas_por_genero[genero]):
            text = font.render(f'{idx + 1} - {nome_musica}', True, BLACK)
            screen.blit(text, (100, 200 + idx * 50))
        text = font.render('P - Play/Pause / Setas - Volume', True, BLACK)
        screen.blit(text, (100, 300 + len(musicas_por_genero[genero]) * 50))
        text = font.render('Q - Voltar', True, BLACK)
        screen.blit(text, (50, 50))
    pygame.display.update()

def play_pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_program()

        if menu:
            # Verifica se algum botão foi clicado
            for button in buttons_menu:
                if button.is_clicked(event):
                    break

        elif music_menu:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2]:
                    musica_idx = event.key - pygame.K_1
                    if musica_idx < len(musicas_por_genero[genero]):
                        musica, music_file = musicas_por_genero[genero][musica_idx]
                elif event.key == pygame.K_p and music_file:
                    if pygame.mixer.music.get_busy():
                        play_pause_music()
                    else:
                        play_music(music_file)
                elif event.key == pygame.K_q:
                    music_menu = False
                    menu = True

    # Desenha o menu ou o menu de música
    if menu:
        draw_menu()
    elif music_menu:
        draw_music_menu()

    pygame.display.update()
    pygame.time.Clock().tick(60)
