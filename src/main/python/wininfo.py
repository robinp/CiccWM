class WinInfo:

    def __init__(self, win):
        self.win = win
        self.savedStyle = self.win.getStyle()
        self.managed = False
        print("savedStyle:", self.savedStyle)

    def getWin(self):
        return self.win

    def isManaged(self):
        return self.managed

    def setManaged(self, b):
        self.managed = b

    def manage(self):
        print("manage")
        self.setManaged(True)

    def unmanage(self):
        print("unmanage")
        self.setManaged(False)
        #self.win.setStyle(self.savedStyle)
