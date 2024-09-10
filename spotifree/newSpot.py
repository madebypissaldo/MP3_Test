import pygame
import sys
import yt_dlp
import os
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import stat
from youtubesearchpython import VideosSearch
import shutil

pygame.init()
SONG_END = pygame.USEREVENT + 1  # Evento personalizado para o final da música

class Spotify(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_song_path = None  # Caminho da música atual
        self.song_index = 0  # Índice da música atual
        pygame.mixer.music.set_endevent(SONG_END)  # Definir o evento ao término da música
        
        self.title('Spotify')
        self.geometry('800x350')
        
        pygame.mixer.init()
        pygame.init()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#E1D7C3')
        self.style.configure('TButton', background = '#5E503F', foreground = 'black', borderwidth = 0, relief = 'flat', font = ('arial', 14))
        self.style.map('TButton', background=[('active', '#786D5F')])
        self.style.configure('TLabel', background='#E1D7C3', foreground='#5E503F', font=('Arial', 12))
        self.style.configure('TEntry', background='white', foreground='#5E503F', font=('Arial', 14))
        self.style.configure('TText', background='white', foreground='#5E503F', font=('Arial', 12))
        self.style.configure('Vertical.TScrollbar', background='#5E503F')

        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=1, padx=20, pady=20)
        
        # Left frame for display area
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side='left', fill='both', expand=1)
        
        # Right frame for buttons and entry
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side='right', fill='y')
        
        # Entry widget and search button frame
        self.entry_frame = ttk.Frame(self.right_frame)
        self.entry_frame.pack(padx=20, pady=20)
        
        self.entry = ttk.Entry(master=self.entry_frame, width=20, font=('Arial', 14))
        self.entry.pack(side="left", padx=(0, 10))

        self.search_button = ttk.Button(master=self.entry_frame, text="Search Song", command=self.search_song, width=15)
        self.search_button.pack(side="left")

        # Buttons
        # self.shuffle_button = ttk.Button(master=self.right_frame, text="Shuffle", command=self.shuffle_songs, width=15)
        # self.shuffle_button.pack(pady=10, padx=20)

        self.playlist_button = ttk.Button(master=self.right_frame, text="Playlist", command=self.view_songs, width=15)
        self.playlist_button.pack(pady=10, padx=20)

        # self.play_songs_button = ttk.Button(master=self.right_frame, text="Play", command=self.play_songs, width=15)
        # self.play_songs_button.pack(pady=10, padx=20)

        # Display area for song list and scrollbar
        self.display_songs_text = tk.Text(master=self.left_frame, wrap="none", width=40)
        self.display_songs_text.pack(pady=20, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(master=self.left_frame, command=self.display_songs_text.yview, style='Vertical.TScrollbar')
        self.scrollbar.pack(side="right", fill="y")

        self.display_songs_text.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Função para baixar o áudio do YouTube
    def download_youtube(self, song_info):
        download_directory = "downloaded_songs"
        
        # Criar o diretório se não existir
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        index = song_info['id']
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_directory, f'{index}-%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        url = song_info['url']
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
            ydl.download([url])
            filename = ydl.prepare_filename(info_dict)

            # Garantir que a extensão seja .mp3
            if not filename.endswith('.mp3'):
                filename = os.path.splitext(filename)[0] + '.mp3'
            return filename  # Retornar o caminho do arquivo MP3
        
    # Função que lida com a reprodução da próxima música
    def play_next_song(self):
        self.song_index += 1
        if self.song_index < len(self.youtube_results):
            next_song_info = self.youtube_results[self.song_index]
            if not next_song_info['file_path']:
                music_file = self.download_youtube(next_song_info['url'])
                next_song_info['file_path'] = music_file
            else:
                music_file = next_song_info['file_path']
            self.play_song(music_file)
        else:
            print("Fim da lista de músicas.")

    # Função para tocar a música baixada
    def play_song(self, song_path):
        self.current_song_path = song_path
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        # Aguardar até a música terminar antes de prosseguir
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    # Exibir e tocar as músicas em sequência
    def view_songs(self):
        for song_info in self.youtube_results:
            self.download_youtube(song_info)

    # Função para baixar e tocar uma música de forma assíncrona
    def download_and_play_youtube(self, song_info):
        def play():
            try:
                # Se já houver uma música tocando, deletar o áudio temporário anterior
                if pygame.mixer.music.get_busy():
                    self.delete_temp_audio()

                # Baixar a nova música se ainda não foi baixada
                if not song_info['file_path']:
                    music_file = self.download_youtube(song_info)
                    song_info['file_path'] = music_file  # Atualizar o caminho do arquivo na lista
                else:
                    music_file = song_info['file_path']

                # Tocar a música baixada
                self.play_song(music_file)
            except Exception as e:
                print(f"Erro ao tocar o áudio do YouTube: {e}")

        threading.Thread(target=play).start()

    # Função para deletar o arquivo de áudio temporário
    def delete_temp_audio(self):
        download_directory = 'downloaded_songs'
    
        # Verificar se o diretório existe
        if os.path.exists(download_directory):
            # Iterar sobre todos os arquivos no diretório
            for file_name in os.listdir(download_directory):
                file_path = os.path.join(download_directory, file_name)
                
                # Tornar o arquivo gravável e excluí-lo
                if os.path.isfile(file_path):
                    os.chmod(file_path, stat.S_IWRITE)  # Garantir que o arquivo seja gravável
                    os.remove(file_path)  # Excluir o arquivo
        pygame.mixer.music.unload()  # Descarregar o mixer

    # Play music from YouTube
    def search_song(self):
        search_query = self.entry.get()
        if not search_query:
            messagebox.showerror("Error", "Please enter a search term!")
            return
        
        # Search for the video on YouTube
        def search_videos():
            videos_search = VideosSearch(search_query, limit=5)
            results = videos_search.result()["result"]

            # If results are found
            if results:
                self.display_songs_text.delete("1.0", tk.END)
                self.youtube_results = []
                for index, video in enumerate(results, 1):
                    video_title = video['title']
                    video_url = video['link']
                    
                    # Armazenar as informações em um dicionário
                    song_info = {
                        'id': index,
                        'title': video_title,
                        'url': video_url,
                        'file_path': None  # Será preenchido após o download
                    }
                    self.youtube_results.append(song_info)

                    # Display each result as a button
                    button = ttk.Button(
                        master=self.display_songs_text,
                        text=f"{index}. {video_title}",
                        command=lambda url=video_url: self.download_and_play_youtube(url),
                        width=50, style='TButton'
                    )
                    self.display_songs_text.window_create(tk.END, window=button)
                    self.display_songs_text.insert(tk.END, "\n")
            else:
                self.display_songs_text.insert(tk.END, "No results found.")

            self.display_songs_text.update_idletasks()
            self.scrollbar.update_idletasks()
            self.display_songs_text.yview_moveto(0.0)

        threading.Thread(target=search_videos).start()
        
    # Loop para ouvir o evento de término da música e tocar a próxima
    def event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == SONG_END:
                    self.play_next_song()

    # Handle closing of the window
    def on_closing(self):
        self.delete_temp_audio()
        pygame.quit()
        self.destroy()

if __name__ == '__main__':
    app = Spotify()
    app.mainloop()