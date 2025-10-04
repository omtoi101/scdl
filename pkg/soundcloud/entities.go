package soundcloud

// AudioLink struct for unmarshalling data
type AudioLink struct {
	URL string `json:"url"`
}

// Track represents a single track.
type Track struct {
	ID           int    `json:"id"`
	PermalinkURL string `json:"permalink_url"`
}

// Playlist represents a playlist of tracks.
type Playlist struct {
	Tracks []Track `json:"tracks"`
}
