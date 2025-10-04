from pathlib import Path

"""
    Format MP3 file name into 'Artist - SongName' style.
    
    Rules:
    - Remove file extension
    - Replace underscores with spaces
    - Try to split into 'Artist - SongName' if '-' is found
    - If no '-' present, just return the cleaned name
"""

def formatName(file: Path) -> str:
    
    name = file.stem                                    #get file name without extension
    name.replace('_', ' ')                              #replace all "_" by " "

    name = ' '.join(name.split())                       #join separate word with " "
    
    if '-' in name:
        artist, song = name.split('-', 1)               #split the title into artist and song
        artist.strip().title(); song.strip().title()    #Make each title formatted
        return f"{artist} - {song}"                     #Return the full title

    else:
        artist, song = name.split(' ', 1)               #split the title into artist and song
        artist.strip().title(); song.strip().title()    #Make each title formatted
        return f"{artist} - {song}"                     #Return the full title