import native

from keyevent import KeyEvent
from keycode import KeyCode
from wininfo import WinInfo
from columns import Columns
import layout

class CiccWm:

    def __init__(self, keyOp, winOp):
        self.keyOp = keyOp
        self.winOp = winOp
        self.windows = {}
        self.columns = Columns()

    def start(self):
        self.keyOp.setUserKeyListener(self.keyListener_)
        for (cb, key, mods) in [
            (self.onCycleLeft_,     'H', ['alt']),
            (self.onCycleDown_,     'J', ['alt']),
            (self.onCycleUp_,       'K', ['alt']),
            (self.onCycleRight_,    'L', ['alt']),

            (self.onShiftLeft_,     'H', ['alt', 'shift']),
            (self.onShiftDown_,     'J', ['alt', 'shift']),
            (self.onShiftUp_,       'K', ['alt', 'shift']),
            (self.onShiftRight_,    'L', ['alt', 'shift']),
        ]:
            self.keyOp.addHotkeyListener(
                cb, ord(key),
                withWin = 'win' in mods,
                withAlt = 'alt' in mods,
                withShift = 'shift' in mods,
                withCtrl = 'ctrl' in mods)

        self.keyOp.startEvents()

    def quit(self):
        self.keyOp.stopEvents()

    def windowListener_(self, win):
        if win not in self.windows:
            self.newWindow_(win)

    def newWindow_(self, win):
        wi = WinInfo(win)

        self.windows[win] = wi

    def getWi(self, win):
        return self.windows[win]

    def startManaging_(self, win):
        wi = self.getWi(win)

        if wi.isManaged():
            return

        wi.manage()
        self.columns.addAsRow(wi)

    def onCycleUp_(self):
        self.columns.cycleUpActCol()
        self.columns.doLayout()
    
    def onCycleDown_(self):
        self.columns.cycleDownActCol()
        self.columns.doLayout()

    def onCycleRight_(self):
        self.columns.cycleRight()
        self.columns.doLayout()
    
    def onCycleLeft_(self):
        self.columns.cycleLeft()
        self.columns.doLayout()

    def onShiftUp_(self):
        self.columns.shiftUpActWin()
        self.columns.doLayout()
    
    def onShiftDown_(self):
        self.columns.shiftDownActWin()
        self.columns.doLayout()

    def onShiftRight_(self):
        self.columns.shiftRightActWin()
        self.columns.doLayout()
    
    def onShiftLeft_(self):
        self.columns.shiftLeftActWin()
        self.columns.doLayout()

    def keyListener_(self, ev):
        if ev.keyId in KeyCode.MODIFIERS or not ev.isPress:
            return True

        """
        print("key press: {0}, id: {1}, alt: {alt}, ctrl: {ctrl}, shift: {shift}, window: {wincap})".format(
            ev.isPress, ev.keyId, alt=ev.withAlt, ctrl=ev.withCtrl,
            shift=ev.withShift, wincap=ev.forWindow.getCaption()) )

        """

        self.windowListener_(ev.forWindow)

        if ev.withAlt and ev.withShift and ev.keyId == ord('Q'):
            self.quit()
            return False

        if ev.withAlt and ev.withShift and ev.keyId == ord('A'):
            self.startManaging_(ev.forWindow)
            self.columns.doLayout()
            return False
        
        if ev.withAlt and ev.withShift and ev.keyId == ord('M'):
            self.columns.setActColLayout(layout.MaxingLayout())
            self.columns.doLayout()
            return False

        if ev.withAlt and ev.withShift and ev.keyId == ord('D'):
            self.columns.setActColLayout(layout.DistributingLayout())
            self.columns.doLayout()
            return False

        if ev.withAlt and ev.withShift and ev.keyId == ord('S'):
            self.columns.setActColLayout(layout.StackLayout())
            self.columns.doLayout()
            return False

        #if ev.withAlt and ev.keyId == ord('K'):
        #    self.columns.cycleUpActCol()
        #    return False

        
        if ev.withAlt and ev.withShift and ev.keyId == ord('R'):
            print("Layout")
            self.columns.doLayout()
            return False        

        return True

def main():
    keyOp = native.getKeyOp()
    winOp = native.getWinOp()
    ciccwm = CiccWm(keyOp, winOp)
    ciccwm.start()

main()
