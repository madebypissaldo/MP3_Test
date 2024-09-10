import pygame
import sys
import yt_dlp
import os
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import stat

pygame.init()

# YouTube music download settings
def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return 'temp_audio.mp3'

def delete_temp_audio():
    temp_audio_path = 'temp_audio.mp3'
    if os.path.exists(temp_audio_path):
        os.chmod(temp_audio_path, stat.S_IWRITE)
        os.remove(temp_audio_path)
        pygame.mixer_music.unload()

FOLDER_PATH = 'C:/Users/gabriel/Desktop/Programas/python/mp3project/Playlist'

# If the folder exists, list songs, otherwise keep empty
if os.path.exists(FOLDER_PATH):
    MY_SONGS = os.listdir(FOLDER_PATH)
else:
    MY_SONGS = []

class Spotify(tk.Tk):
    def __init__(self):
        super().__init__()
        
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
        self.shuffle_button = ttk.Button(master=self.right_frame, text="Shuffle", command=self.shuffle_songs, width=15)
        self.shuffle_button.pack(pady=10, padx=20)

        self.playlist_button = ttk.Button(master=self.right_frame, text="Playlist", command=self.view_songs, width=15)
        self.playlist_button.pack(pady=10, padx=20)

        self.play_songs_button = ttk.Button(master=self.right_frame, text="Play", command=self.play_songs, width=15)
        self.play_songs_button.pack(pady=10, padx=20)

        # Button for YouTube music
        self.youtube_button = ttk.Button(master=self.right_frame, text="Play from YouTube", command=self.play_youtube_song, width=20)
        self.youtube_button.pack(pady=10, padx=20)

        # Display area for song list and scrollbar
        self.display_songs_text = tk.Text(master=self.left_frame, wrap="none", width=40)
        self.display_songs_text.pack(pady=20, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(master=self.left_frame, command=self.display_songs_text.yview, style='Vertical.TScrollbar')
        self.scrollbar.pack(side="right", fill="y")

        self.display_songs_text.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Search for a song
    def search_song(self):
        self.display_songs_text.delete("1.0", tk.END)
        user_entry = self.entry.get().lower()
        searched_songs = [s for s in MY_SONGS if user_entry in s.lower()]

        if searched_songs:
            for song in searched_songs:
                button = ttk.Button(master=self.display_songs_text, text=song, command=lambda s=song: self.play_selected_song(s), width=25, style='TButton')
                self.display_songs_text.window_create(tk.END, window=button)
                self.display_songs_text.insert(tk.END, "\n")
        else:
            self.display_songs_text.insert(tk.END, "Song not found")

        self.display_songs_text.update_idletasks()
        self.scrollbar.update_idletasks()
        self.display_songs_text.yview_moveto(0.0)

    # Shuffle the playlist
    def shuffle_songs(self):
        random.shuffle(MY_SONGS)
        self.display_songs_text.delete("1.0", tk.END)

        for song in MY_SONGS:
            button = ttk.Button(master=self.display_songs_text, text=song, command=lambda s=song: self.play_selected_song(s), width=25, style='TButton')
            self.display_songs_text.window_create(tk.END, window=button)
            self.display_songs_text.insert(tk.END, "\n")

        self.display_songs_text.update_idletasks()
        self.scrollbar.update_idletasks()
        self.display_songs_text.yview_moveto(0.0)

    # View songs in playlist
    def view_songs(self):
        self.display_songs_text.delete("1.0", tk.END)

        for song in MY_SONGS:
            button = ttk.Button(master=self.display_songs_text, text=song, command=lambda s=song: self.play_selected_song(s), width=25, style='TButton')
            self.display_songs_text.window_create(tk.END, window=button)
            self.display_songs_text.insert(tk.END, "\n")

        self.display_songs_text.update_idletasks()
        self.scrollbar.update_idletasks()
        self.display_songs_text.yview_moveto(0.0)

    # Play selected local song
    def play_selected_song(self, song):
        song_path = os.path.join(FOLDER_PATH, song)

        def play():
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()

            except Exception as e:
                print(f"Error playing {song}: {e}")

        threading.Thread(target=play).start()

    # Play songs in order displayed on the screen
    def play_songs(self):
        button_names = [button.cget("text") for button in self.display_songs_text.winfo_children()]

        def play_next_song(song_paths):
            if song_paths:
                song_path = song_paths.pop(0)
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    pygame.mixer.music.load(song_path)
                    pygame.mixer.music.play()

                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                    self.after(100, check_event, song_paths)

                except Exception as e:
                    print(f"Error playing {song_path}: {e}")

        def check_event(song_paths):
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    play_next_song(song_paths)

            self.after(100, check_event, song_paths)

        threading.Thread(target=play_next_song, args=([os.path.join(FOLDER_PATH, s) for s in button_names],)).start()

    # Play music from YouTube
    def play_youtube_song(self):
        url = self.entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL!")
            return

        def play():
            try:
                if pygame.mixer.music.get_busy():
                    delete_temp_audio()
                music_file = download_youtube_audio(url)
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing YouTube audio: {e}")

        threading.Thread(target=play).start()

    # Handle closing of the window
    def on_closing(self):
        #delete_temp_audio()
        #pygame.mixer.music.stop()
        pygame.quit()
        self.destroy()

if __name__ == '__main__':
    app = Spotify()
    app.mainloop()
