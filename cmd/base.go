package cmd

import (
	"fmt"
	"github.com/imthaghost/scdl/pkg/soundcloud"
	"log"
)

func scdl(args []string) {
	url := args[0]

	// Create a new SoundCloud client
	sc := soundcloud.NewClient("", nil)

	if Playlist {
		playlist, err := sc.GetPlaylist(url)
		if err != nil {
			log.Fatalf("failed to get playlist: %v", err)
		}

		fmt.Printf("Downloading %d tracks from playlist...\n", len(playlist.Tracks))

		for _, track := range playlist.Tracks {
			fmt.Printf("Downloading track: %s\n", track.PermalinkURL)
			sc.Download(track.PermalinkURL)
		}

		fmt.Println("Playlist download complete.")
	} else {
		// Download the song
		sc.Download(url)
	}
}
