import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import ttk
from ttkthemes import ThemedTk
import pygame
import webbrowser
from pytube import YouTube

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x600")

        pygame.init()
        pygame.mixer.init()

        self.playlist = []
        self.current_song = 0

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use("clearlooks")  # Light theme as default

        label_title = ttk.Label(self.root, text="Music Player", font=("Helvetica", 20))
        label_title.pack(pady=10)

        # Custom style for the buttons
        self.style.configure("TButton", font=("Helvetica", 12), padding=10, relief="raised", foreground="black")
        self.style.map("TButton",
                       foreground=[('active', 'blue'), ('pressed', 'red')])

        # Frame for horizontal buttons
        btn_frame_horizontal = ttk.Frame(self.root)
        btn_frame_horizontal.pack(side=tk.TOP, pady=10)

        # Horizontal buttons
        btn_add_music = ttk.Button(btn_frame_horizontal, text="Add Music", command=self.add_music, style="TButton")
        btn_add_music.pack(side=tk.LEFT, padx=5)

        btn_play_music = ttk.Button(btn_frame_horizontal, text="Play Music", command=self.play_music, style="TButton")
        btn_play_music.pack(side=tk.LEFT, padx=5)

        btn_stop_music = ttk.Button(btn_frame_horizontal, text="Stop Music", command=self.stop_music, style="TButton")
        btn_stop_music.pack(side=tk.LEFT, padx=5)

        btn_next = ttk.Button(btn_frame_horizontal, text="Next", command=self.play_next, style="TButton")
        btn_next.pack(side=tk.LEFT, padx=5)

        btn_back = ttk.Button(btn_frame_horizontal, text="Back", command=self.play_previous, style="TButton")
        btn_back.pack(side=tk.LEFT, padx=5)

        # Frame for vertical buttons
        btn_frame_vertical = ttk.Frame(self.root)
        btn_frame_vertical.pack(side=tk.TOP, pady=10)

        # Vertical buttons
        btn_play_video = ttk.Button(btn_frame_vertical, text="Open YouTube Link", command=self.open_youtube_link, style="TButton")
        btn_play_video.pack(pady=5)

        btn_download_mp3 = ttk.Button(btn_frame_vertical, text="Download MP3", command=self.download_mp3, style="TButton")
        btn_download_mp3.pack(pady=5)

        btn_download_mp4 = ttk.Button(btn_frame_vertical, text="Download MP4", command=self.download_mp4, style="TButton")
        btn_download_mp4.pack(pady=5)

        # Dark/Light Mode Button
        self.btn_mode_toggle = ttk.Button(self.root, text="Dark Mode", command=self.toggle_mode)
        self.btn_mode_toggle.pack(side=tk.RIGHT, padx=10, pady=10)

    def add_music(self):
        file_paths = filedialog.askopenfilenames(initialdir="./music", title="Select Music", filetypes=(("Audio Files", "*.mp3"),))
        if file_paths:
            self.playlist.extend(file_paths)

    def play_music(self):
        if not self.playlist:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        song = self.playlist[self.current_song]

        # Check if the file is an MP3 file before trying to load it
        if os.path.splitext(song)[1].lower() != ".mp3":
            print(f"Error: File '{song}' is not an MP3 file.")
            return

        try:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error loading the MP3 file: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_next(self):
        if not self.playlist:
            return

        self.current_song = (self.current_song + 1) % len(self.playlist)
        self.play_music()

    def play_previous(self):
        if not self.playlist:
            return

        self.current_song = (self.current_song - 1) % len(self.playlist)
        self.play_music()

    def open_youtube_link(self):
        youtube_link = simpledialog.askstring("YouTube Link", "Enter the YouTube link:")
        if youtube_link:
            webbrowser.open(youtube_link)

    def download_mp3(self):
        youtube_link = simpledialog.askstring("YouTube Link", "Enter the YouTube link:")
        if youtube_link:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True).first()
            download_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
            if download_path:
                stream.download(output_path=os.path.dirname(download_path), filename=os.path.basename(download_path))

    def download_mp4(self):
        youtube_link = simpledialog.askstring("YouTube Link", "Enter the YouTube link:")
        if youtube_link:
            yt = YouTube(youtube_link)
            stream = yt.streams.filter(only_video=True).first()
            download_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
            if download_path:
                stream.download(output_path=os.path.dirname(download_path), filename=os.path.basename(download_path))

    def toggle_mode(self):
        current_theme = self.style.theme_use()
        if current_theme == "clearlooks":
            self.style.theme_use("alt")
            self.btn_mode_toggle.config(text="Light Mode")
        else:
            self.style.theme_use("clearlooks")
            self.btn_mode_toggle.config(text="Dark Mode")

        # Update the style settings for all widgets
        self.update_widget_style(self.root)

    def update_widget_style(self, widget):
        widget_style = widget.winfo_class()
        if widget_style == "TButton":
            widget.config(style=widget_style)
        elif widget_style == "TLabel":
            if self.style.theme_use() == "clearlooks":
                widget.config(foreground="black", background="SystemButtonFace")
            else:
                widget.config(foreground="white", background="black")

        # Recursively update style for children widgets
        for child in widget.winfo_children():
            self.update_widget_style(child)

if __name__ == "__main__":
    root = ThemedTk(theme="clearlooks")
    music_player = MusicPlayer(root)
    root.mainloop()


# All Copyright By Savindu Deshan
