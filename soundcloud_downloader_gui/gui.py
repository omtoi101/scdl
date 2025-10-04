import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from config import Config
from downloader import Downloader

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SoundCloud Playlist Downloader")
        self.geometry("500x400")

        self.config = Config()
        self.downloader = Downloader(self.config.get("download_dir"))

        self.create_widgets()
        self.update_playlist_listbox()

    def create_widgets(self):
        # Frame for adding playlists
        add_frame = tk.Frame(self)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Playlist URL:").pack(side=tk.LEFT)
        self.playlist_url_entry = tk.Entry(add_frame, width=40)
        self.playlist_url_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(add_frame, text="Add", command=self.add_playlist).pack(side=tk.LEFT)

        # Frame for the playlist listbox
        list_frame = tk.Frame(self)
        list_frame.pack(pady=10)

        tk.Label(list_frame, text="Auto-updating Playlists:").pack()
        self.playlist_listbox = tk.Listbox(list_frame, width=60, height=10)
        self.playlist_listbox.pack()

        # Frame for buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Remove Selected", command=self.remove_playlist).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Change Download Folder", command=self.change_download_dir).pack(side=tk.LEFT, padx=5)
        self.update_button = tk.Button(button_frame, text="Update All Playlists", command=self.update_all_playlists)
        self.update_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack()

    def add_playlist(self):
        playlist_url = self.playlist_url_entry.get()
        if playlist_url:
            self.config.add_playlist(playlist_url)
            self.update_playlist_listbox()
            self.playlist_url_entry.delete(0, tk.END)
            self.status_label.config(text=f"Added playlist: {playlist_url}")
        else:
            messagebox.showwarning("Warning", "Please enter a playlist URL.")

    def remove_playlist(self):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            playlist_url = self.playlist_listbox.get(selected_index)
            self.config.remove_playlist(playlist_url)
            self.update_playlist_listbox()
            self.status_label.config(text=f"Removed playlist: {playlist_url}")
        else:
            messagebox.showwarning("Warning", "Please select a playlist to remove.")

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.config.get("playlists"):
            self.playlist_listbox.insert(tk.END, playlist)

    def change_download_dir(self):
        new_dir = filedialog.askdirectory()
        if new_dir:
            self.config.set("download_dir", new_dir)
            self.downloader = Downloader(new_dir)
            self.status_label.config(text=f"Download directory changed to: {new_dir}")

    def update_all_playlists(self):
        playlists = self.config.get("playlists")
        if playlists:
            self.status_label.config(text="Updating playlists...")
            self.update_button.config(state=tk.DISABLED)
            download_thread = threading.Thread(target=self._download_worker, args=(playlists,), daemon=True)
            download_thread.start()
        else:
            messagebox.showinfo("Info", "No playlists to update.")

    def _download_worker(self, playlists):
        results = self.downloader.update_playlists(playlists)
        self.after(0, self._on_download_complete, results)

    def _on_download_complete(self, results):
        self.status_label.config(text="Update complete.")
        self.update_button.config(state=tk.NORMAL)
        messagebox.showinfo("Update Results", results)