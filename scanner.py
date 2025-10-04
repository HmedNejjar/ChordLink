from pathlib import Path
import os


class MP3Manager:
    def __init__(self, folderName = "Songs"):
        # Initialize MP3Manager: set base dir, target folder name and ensure folder exists
        self.dir = Path("C:/Users/Public/Music")
        self.folderName = folderName
        self.musicFolder = self.dir / self.folderName
        
        self.createFolder()
        
    def createFolder(self):
        # Create the main music folder on disk (creates parent directories if needed)
        self.musicFolder.mkdir(parents=True, exist_ok=True)
        print(f"Folder created at {self.musicFolder}")
        
    def getMP3(self) -> list:
        # Return a list of Path objects for MP3 files in the musicFolder (case-insensitive)
        mp3_files = list(self.musicFolder.glob('*.[mM][pP]3'))
        return mp3_files
    
    