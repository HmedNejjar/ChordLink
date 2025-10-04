from pathlib import Path
import pygame

"""Player module for ChordLink.

Initializes pygame.mixer and manages a simple playlist.
Provides functions to load songs, play/pause/resume, navigate tracks,
and automatically advance when a song ends (via pygame event).
"""

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Global variables to maintain state across function calls
playlist: list[Path] = []          # Stores all loaded MP3 file paths
currentSongIndex = -1              # Tracks currently playing song (-1 = none)
is_paused = False                  # Flag to track if music is currently paused

# Set up custom event to detect when a song ends
SONG_END = pygame.USEREVENT + 1    # Create unique event ID for song completion
pygame.mixer.music.set_endevent(SONG_END)  # Tell pygame to trigger this event when song ends

def loadSongs(songsList: list[Path]):
    """Load songs into the playlist and initialize player"""
    songs = [song for song in songsList if song.suffix == '.mp3' and song.exists()] #Load all songs in the playlist in this list
    print(f"Loaded {len(songs)} songs")

def Play(index):
    """Play a specific song from the playlist"""
    global playlist, currentSongIndex, is_paused
    
    if not playlist:
        print("Playlist is empty")
        return
    
    if 0 <= index < len(playlist):      
        pygame.mixer.music.load(str(playlist[index]))   # Load the MP3 file into pygame mixer
        pygame.mixer.music.play()                       # Start playback of loaded song
        currentSongIndex = index                        # Update global tracker to current song
        is_paused = False                              # Reset pause state when new song starts
        print(f"Playing: {playlist[currentSongIndex]}") # Notify user what's playing
    
    else:
        print("Invalid song index")                     # Error handling for bad index

def PlayNext():
    """Play the next song in the playlist (wraps around to beginning)"""
    global playlist, currentSongIndex
    
    if playlist:
        nextSong = (currentSongIndex + 1) % len(playlist)   # Calculate next index with wrap-around using modulo
        Play(nextSong)                                      # Call Play function with new index

def PlayPrevious():
    """Play the previous song in the playlist (wraps around to end)"""
    global playlist, currentSongIndex
    
    if playlist:
        previousSong = (currentSongIndex - 1) % len(playlist)   # Calculate previous index with wrap-around
        Play(previousSong)                                      # Call Play function with previous index

def Pause():
    """Pause the currently playing music"""
    global is_paused
    if pygame.mixer.music.get_busy() and not is_paused:  # Check if music is actually playing and not already paused
        pygame.mixer.music.pause()                       # Tell pygame to pause playback
        is_paused = True                                # Update global pause state
        print("Music paused")
    else:
        print("No music is playing or already paused")   # Inform user if pause is not possible

def Resume():
    """Resume paused music"""
    global is_paused
    if is_paused:                                       # Check if music was actually paused
        pygame.mixer.music.unpause()                    # Tell pygame to resume playback from where it left off
        is_paused = False                              # Update global pause state
        print("Music resumed")
    else:
        print("Music is not paused")                    # Inform user if resume is not possible

def TogglePlayPause():
    """Toggle pause/resume or start playback without forcing first track restart."""
    global is_paused, currentSongIndex, playlist
    try:
        # If currently paused, unpause
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
            print("Music resumed")
            return "resumed"
        # If currently playing, pause
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            is_paused = True
            print("Music paused")
            return "paused"
        # If nothing is playing but we have a current index, (re)start that song
        if currentSongIndex >= 0 and 0 <= currentSongIndex < len(playlist):
            pygame.mixer.music.load(str(playlist[currentSongIndex]))
            pygame.mixer.music.play()
            is_paused = False
            print("Music started")
            return "started"
        # If no current song selected, start the first available
        if playlist:
            Play(0)
            return "started"
        print("Playlist is empty")
        return "no_songs"
    except pygame.error as e:
        print(f"Audio error: {e}")
        return "error"

def AutoNextSong():
    """Check for song end events and automatically play next song"""
    for event in pygame.event.get():                    # Check all pygame events in the queue
        if event.type == SONG_END:                     # Look for our custom song end event
            print("Song finished, playing next...")    # Notify user of auto-advance
            PlayNext()                                 # Automatically start next song