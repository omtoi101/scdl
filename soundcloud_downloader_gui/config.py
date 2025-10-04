import os
import json
from appdirs import user_config_dir

class Config:
    def __init__(self):
        self.config_dir = user_config_dir("SoundCloudDownloaderGUI", "Jules")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = self.load_config()

    def load_config(self):
        """Loads the configuration from the config file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                "download_dir": os.path.join(os.path.expanduser("~"), "Music", "SoundCloudDownloader"),
                "playlists": []
            }

    def save_config(self):
        """Saves the current configuration to the config file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        """Gets a value from the configuration."""
        return self.config.get(key)

    def set(self, key, value):
        """Sets a value in the configuration."""
        self.config[key] = value
        self.save_config()

    def add_playlist(self, playlist_url):
        """Adds a playlist to the list of playlists."""
        if playlist_url not in self.config["playlists"]:
            self.config["playlists"].append(playlist_url)
            self.save_config()

    def remove_playlist(self, playlist_url):
        """Removes a playlist from the list of playlists."""
        if playlist_url in self.config["playlists"]:
            self.config["playlists"].remove(playlist_url)
            self.save_config()