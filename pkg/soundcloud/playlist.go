package soundcloud

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

// PlaylistService handles communication with the playlist related
// methods of the SoundCloud API.
//
// SoundCloud API docs: https://developers.soundcloud.com/docs/api/reference#playlists
type PlaylistService service

// GetPlaylist fetches a playlist from a given URL.
func (s *Soundcloud) GetPlaylist(url string) (*Playlist, error) {
	clientID, err := s.GetClientID()
	if err != nil {
		return nil, fmt.Errorf("failed to get client ID: %v", err)
	}

	// Resolve the URL to get the playlist ID
	resolveURL := fmt.Sprintf("https://api-v2.soundcloud.com/resolve?url=%s&client_id=%s", url, clientID)
	resp, err := http.Get(resolveURL)
	if err != nil {
		return nil, fmt.Errorf("failed to resolve URL: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	var resolved struct {
		ID int `json:"id"`
	}
	if err := json.Unmarshal(body, &resolved); err != nil {
		return nil, fmt.Errorf("failed to unmarshal resolved response: %v", err)
	}

	// Fetch the playlist data
	playlistURL := fmt.Sprintf("https://api-v2.soundcloud.com/playlists/%d?client_id=%s", resolved.ID, clientID)
	resp, err = http.Get(playlistURL)
	if err != nil {
		return nil, fmt.Errorf("failed to get playlist: %v", err)
	}
	defer resp.Body.Close()

	body, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read playlist body: %v", err)
	}

	var playlist Playlist
	if err := json.Unmarshal(body, &playlist); err != nil {
		return nil, fmt.Errorf("failed to unmarshal playlist: %v", err)
	}

	return &playlist, nil
}