from soundcloud_downloader import SoundCloudDownloader
from soundcloud_downloader.scdl import Scdl
import os

class Downloader:
    def __init__(self, download_dir):
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        # We manually create Scdl to have more control
        self.scdl = Scdl(output=download_dir)

    def download_playlist(self, playlist_url):
        """Downloads a single playlist."""
        try:
            # The download_playlist method is not directly available on Scdl,
            # so we use the generic download method.
            self.scdl.download([playlist_url])
            return True, f"Successfully downloaded playlist: {playlist_url}"
        except Exception as e:
            # The library does not expose specific exceptions, so we catch a generic one.
            # We can check for common error messages in the string representation of e
            error_str = str(e).lower()
            if "not a valid soundcloud url" in error_str:
                return False, f"Invalid SoundCloud URL: {playlist_url}"
            elif "404 client error" in error_str:
                return False, f"Playlist not found (404): {playlist_url}"
            else:
                return False, f"Failed to download playlist: {playlist_url}. Error: {e}"

    def update_playlists(self, playlist_urls):
        """Updates all playlists from a list of URLs."""
        results = []
        for url in playlist_urls:
            success, message = self.download_playlist(url)
            results.append(message)
        return "\n".join(results)