import winop_w32 as winop
import keyop_w32 as keyop

def getWinOp():
    return winop.Winop.getInstance()

def getKeyOp():
    return keyop.Keyop.getInstance()
