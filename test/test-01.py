import pygame
import sys
import yt_dlp
import os
import stat

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

# URLs de vídeos do YouTube
musicas_por_genero = {
    '1': [('Doja - Central Cee', 'https://www.youtube.com/watch?v=_VuJA-VQRcY&pp=ygUQY2VudHJhbCBjZWUgZG9qYQ%3D%3D'),
        ('Irish Drill - AC-130', 'https://www.youtube.com/watch?v=uyHUPhWYRsE&pp=ygUUSXJpc2ggRHJpbGwgLSBBQy0xMzA%3D')],
    '2': [('Bizarrap Session - Peso Pluma', 'https://www.youtube.com/watch?v=v5_SYkFpFiY&pp=ygUdQml6YXJyYXAgU2Vzc2lvbiAtIFBlc28gUGx1bWE%3D'),
        ('TQM - Fuerza Regida', 'https://www.youtube.com/watch?v=DzTNN5Zzpok&pp=ygUTVFFNIC0gRnVlcnphIFJlZ2lkYQ%3D%3D')],
    '3': [('Ivy - Frank Ocean', 'https://www.youtube.com/watch?v=AE005nZeF-A&pp=ygURSXZ5IC0gRnJhbmsgT2NlYW4%3D'),
        ('After Hours - The Weeknd', 'https://www.youtube.com/watch?v=ygTZZpVkmKg&pp=ygUYQWZ0ZXIgSG91cnMgLSBUaGUgV2Vla25k')]
}

# Baixar áudio usando yt-dlp
def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio',
        'ffmpeg_location': r'C:\ffmpeg\bin',  # Caminho para o FFmpeg, se necessário
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return 'temp_audio.mp3'

def play_music_from_youtube(url):
    global music_file
    # Baixa o áudio do YouTube
    music_file = download_youtube_audio(url)
    # Carrega e toca o arquivo baixado
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

def delete_temp_audio():
    # Certifique-se de que a música foi interrompida antes de tentar deletar
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()  # Para a música
    
    # Espera um pouco para garantir que o arquivo foi liberado
    pygame.mixer.music.unload()  # Garante que o arquivo foi completamente descarregado do mixer
    
    # Tenta remover o arquivo após garantir que ele está liberado
    temp_audio_path = 'temp_audio.mp3'
    
    if os.path.exists(temp_audio_path):
        os.chmod(temp_audio_path, stat.S_IWRITE)
        os.remove(temp_audio_path)

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
    delete_temp_audio()
    pygame.quit()
    sys.exit()

# Criando os botões do menu principal
buttons_menu = [
    Button("1 - Drill", 100, 150, 200, 50, GRAY, DARK_GRAY, select_genero_1),
    Button("2 - Corrido Tumbado", 100, 220, 200, 50, GRAY, DARK_GRAY, select_genero_2),
    Button("3 - RnB", 100, 290, 200, 50, GRAY, DARK_GRAY, select_genero_3),
    Button("Sair", 50, 50, 100, 50, GRAY, DARK_GRAY, quit_program)
]

def select_music_1():
    delete_temp_audio()
    global musica, music_menu
    musica = '1'
    music_menu = True
    musica, music_url = musicas_por_genero[genero][0]
    print(musica, music_url)
    play_music_from_youtube(music_url)

def select_music_2():
    delete_temp_audio()
    global musica, music_menu
    musica = '2'
    music_menu = True
    musica, music_url = musicas_por_genero[genero][1]
    print(musica, music_url)
    play_music_from_youtube(music_url)

def voltar():
    global menu, music_menu
    menu = True
    music_menu = False

buttons_music_menu = [[
    Button("1 - Doja - Central Cee", 100, 200, 200, 50, GRAY, DARK_GRAY, select_music_1),
    Button("2 - Irish Drill - AC-130", 100, 300, 200, 50, GRAY, DARK_GRAY, select_music_2),
    Button("Q - Sair", 50, 50, 100, 50, GRAY, DARK_GRAY, voltar)
],
[
    Button("3 - Bizarrap Session - Peso Pluma", 100, 200, 200, 50, GRAY, DARK_GRAY, select_music_1),
    Button("4 - TQM - Fuerza Regida", 100, 300, 200, 50, GRAY, DARK_GRAY, select_music_2),
    Button("Q - Sair", 50, 50, 100, 50, GRAY, DARK_GRAY, voltar)
],
[
    Button("5 - Ivy - Frank Ocean", 100, 200, 200, 50, GRAY, DARK_GRAY, select_music_1),
    Button("6 - After Hours - The Weeknd", 100, 300, 200, 50, GRAY, DARK_GRAY, select_music_2),
    Button("Q - Sair", 50, 50, 100, 50, GRAY, DARK_GRAY, voltar)
]]

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
    for button in buttons_music_menu[int(genero) - 1]:
        button.draw(screen)
        
    text = font.render('SPACE - Play/Pause / Setas - Volume', True, BLACK)
    screen.blit(text, (100, 300 + len(musicas_por_genero[genero]) * 50))
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
            delete_temp_audio()
            quit_program()

        if menu:
            # Verifica se algum botão foi clicado
            for button in buttons_menu:
                if button.is_clicked(event):
                    break

        elif music_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and music_file:
                    play_pause_music()
            for button in buttons_music_menu[int(genero) - 1]:
                if button.is_clicked(event):
                    break

    # Desenha o menu ou o menu de música
    if menu:
        draw_menu()
    elif music_menu:
        draw_music_menu()

    pygame.display.update()
    pygame.time.Clock().tick(60)
