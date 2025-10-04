from pathlib import Path
import pygame

"""Player module for ChordLink.

Initializes pygame.mixer and manages a simple playlist.
Provides functions to load songs, play/pause/resume, navigate tracks,
and automatically advance when a song ends (via pygame event).
"""

pygame.mixer.init()
playlist: list[Path] = []
currentSongIndex = -1

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

def loadSongs(songsList: list[Path]):
    
    songs = [song for song in songsList if song.suffix == '.mp3' and song.exists()] #Load all songs in the playlist in this list
    print(f"Loaded {len(songs)} songs")

def Play(index):
    global playlist, currentSongIndex
    
    if not playlist:
        print("Playlist is empty")
    
    elif 0<= index <= len(playlist):      
        pygame.mixer.music.load(str(playlist[index]))   #Load the first song
        pygame.mixer.music.play()                       #Play the song
        currentSongIndex = index                        #Assign the song's index to the global counter
        print(f"Playing: {playlist[currentSongIndex]}")
    
    else:
        print("Invalid song index")

def PlayNext():
    global playlist, currentSongIndex
    
    if playlist:
        nextSong = (currentSongIndex + 1) % len(playlist)   #Get the next song's index
        Play(nextSong)                                      #Play the song

def PlayPrevious():
    global playlist, currentSongIndex
    
    if playlist:
        previousSong = (currentSongIndex - 1) % len(playlist)   #Get the previous song's index
        Play(previousSong)                                      #Play the song

def Pause():
    pygame.mixer.music.pause()
    print("Music paused")

def Resume():
    pygame.mixer.music.unpause()
    print("Music resumed")

def AutoNextSong():
    for event in pygame.event.get():          #Check if the event "SONG_END" has occured to play next song
        if event.type == SONG_END:
            PlayNext()

    