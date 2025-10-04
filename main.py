from pathlib import Path
from scanner import MP3Manager
from utils import formatName
from player import playlist, currentSongIndex, loadSongs, Play, PlayNext, PlayPrevious, Pause, Resume, AutoNextSong
import sys
import pygame

"""
ChordLink Music Player - Terminal-Based Music Player

This is the main module for ChordLink, a terminal-based music player that:
- Automatically scans for MP3 files in a designated folder
- Provides a simple menu-driven interface for music playback
- Supports play, pause, next, previous, and song selection features
- Uses pygame for audio playback and file management

The program follows a hierarchical menu structure:
1. Main Menu: Entry point with basic options
2. Music Mode: Scans and loads songs, allows initial song selection  
3. Music Control Menu: Provides playback controls while music is playing

Dependencies: pygame, pathlib
"""

# Initialize Pygame video system to avoid "video system not initialized" errors
pygame.init()

def display_main_menu() -> None:
    """Display the main menu options - entry point of the application"""
    print("\n" + "="*50)
    print("          CHORDLINK MUSIC PLAYER")
    print("="*50)
    print("1. Play Music")
    print("2. Exit")
    print("="*50)

def display_music_menu() -> None:
    """Display the player controls menu - handles all playback interactions"""
    while True:  # Keep user in music control mode until they choose to exit
        print("\n" + "-"*50)
        print("PLAYER CONTROLS")
        print("-"*50)
        print("1. Play/Pause")
        print("2. Next Song")
        print("3. Previous Song")
        print("4. Show Playlist & Change Song")
        print("5. Back to Main Menu")
        
        # Display current playback status if a song is loaded
        if currentSongIndex >= 0 and playlist:
            current_song = playlist[currentSongIndex]
            # Check if music is playing - this requires Pygame video system to be initialized
            try:
                status = "▶ Playing" if pygame.mixer.music.get_busy() else "⏸ Paused"
            except pygame.error:
                status = "⏸ Paused"  # Fallback if there's an issue checking playback status
            print(f"\n{status}: {formatName(current_song)}")
        print("-"*50)
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            match (choice):  # Python 3.10+ match case for clean control flow
                case "1":
                    # Play/Pause toggle - check current playback state
                    try:
                        if pygame.mixer.music.get_busy():
                            Pause()
                            print("⏸ Music paused")
                        else:
                            if currentSongIndex >= 0:
                                Resume()
                                print("▶ Music resumed")
                            else:
                                Play(0)  # Start from first song if nothing is playing
                                print("▶ Music started")
                    except pygame.error as e:
                        print(f"Audio error: {e}")
                        # Fallback: if we can't determine state, just try to resume
                        if currentSongIndex >= 0:
                            Resume()
                            print("▶ Music resumed")
                
                case "2":
                    print("⏭ Next song...")
                    PlayNext()  # Advance to next song in playlist
                
                case "3":
                    print("⏮ Previous song...")
                    PlayPrevious()  # Go back to previous song
                
                case "4":
                    displaySongs()  # Show current playlist
                    # Allow song selection after displaying playlist
                    try:
                        song_choice = input(f"Enter song number to play (1-{len(playlist)}) or press Enter to continue: ").strip()
                        if song_choice:
                            song_index = int(song_choice) - 1  # Convert to 0-based index
                            if 0 <= song_index < len(playlist):
                                Play(song_index)  # Play selected song
                    except ValueError:
                        print("Please enter a valid number!")
                
                case "5":
                    print("Returning to main menu...")
                    Pause()  # Pause music when returning to main menu
                    break  # Exit the music control loop
                
                case _:
                    print("Invalid choice! Please enter a number between 1-5.")
            
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            break  # Handle Ctrl+C gracefully
        except Exception as e:
            print(f"An error occurred: {e}")  # Catch any unexpected errors
        
        # Check for song end events to auto-advance to next track
        AutoNextSong()
    
def loadMusic() -> bool:
    """Scan for MP3 files and load them into the player's playlist
    
    Returns:
        bool: True if songs were successfully loaded, False if no songs found
    """
    manager = MP3Manager()  # Create MP3 manager instance
    mp3_playlist = manager.getMP3()  # Scan for MP3 files
    
    if not mp3_playlist:
        print("No MP3 files found in the Songs folder!")
        return False
    
    # Update global playlist with found songs
    playlist.clear()  # Clear any existing songs
    playlist.extend(mp3_playlist)  # Add new songs to playlist
    loadSongs(playlist)  # Load songs into the player module
    return True

def displaySongs() -> None:
    """Display all songs in the current playlist with numbering and current song indicator"""
    if not playlist:
        print("No MP3 files found in the Songs folder!")
        return
    
    print(f"\nPlaylist: ({len(playlist)} songs):")
    for i, song in enumerate(playlist):
        current_indicator = " >>> " if i == currentSongIndex else "     "  # Mark current song
        print(f"{current_indicator}{i+1}. {formatName(song)}")  # Display with 1-based numbering

def MusicMode() -> None:
    """Enter music player mode: scan songs → display → select → control menu"""
    if not loadMusic():  # First, scan and load available songs
        return  # Exit if no songs found
    
    displaySongs()  # Show all available songs to user
    
    # Let user choose initial song to start playback
    while True:
        try:
            choice = input(f"\nEnter song number to play (1-{len(playlist)}): ").strip()
            if choice:
                song_index = int(choice) - 1  # Convert to 0-based index
                if 0 <= song_index < len(playlist):
                    Play(song_index)  # Start playing selected song
                    break  # Exit song selection loop
                else:
                    print(f"Please enter a number between 1 and {len(playlist)}")
            else:
                # If user just presses Enter, default to first song
                Play(0)
                break
        except ValueError:
            print("Please enter a valid number!")
    
    # Enter music control menu after song selection
    display_music_menu()

def main():
    """Main function to run the music player - application entry point"""
    print("Initializing ChordLink Music Player...")
    
    while True:  # Main application loop
        display_main_menu()  # Show main menu options
        
        try:
            choice = input("Enter your choice (1-2): ").strip()
            
            if choice == "1":
                MusicMode()  # Enter music playback mode
            
            elif choice == "2":
                print("Thank you for using ChordLink! Goodbye!")
                pygame.mixer.quit()  # Clean up pygame resources
                pygame.quit()  # Clean up entire pygame system
                sys.exit()  # Exit application
            
            else:
                print("Invalid choice! Please enter 1 or 2.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Shutting down...")
            pygame.mixer.quit()  # Clean up on forced exit
            pygame.quit()  # Clean up entire pygame system
            sys.exit()
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle unexpected errors

if __name__ == "__main__":
    main()  # Start the application