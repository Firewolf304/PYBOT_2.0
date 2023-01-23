#import methods.tools
import os
from pathlib import Path
import methods.funcs as funcs
global mainDir
mainDir = Path(os.getcwd())

class Dirs:
    def __init__(self):
        pass
    def main(self) -> Path:
        return mainDir
    def GetDirs(self) -> iter:
        for i in self.main().iterdir():
            yield i
    def GetDirFromMain(self, nameDir:str) -> Path:
        return Path(self.main(), nameDir)

funcs.funcs()