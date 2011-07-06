"""
Native window wrapper.

"""
import win32gui as wgui
import win32api as wapi
import win32con as wc
import win32process as wproc

import native

class Window:

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.op = {}

    def __eq__(self, other):
        return self.hwnd == other.hwnd

    def __ne__(self, other):
        return not __eq__(self, other)

    def __hash__(self):
        return self.hwnd

    def isAlive(self):
        return wgui.IsWindow(self.hwnd)

    def getCaption(self):
        if not self.isAlive():
            print("Error, window went away!")
            return
        return wgui.GetWindowText(self.hwnd)

    def getRect(self):
        """
        returns (left, top, right, bottom)

        """
        return wgui.GetWindowRect(self.hwnd)

    def getHeight(self):
        l, t, r, b = self.getRect()
        return b - t

    def getTitleBarHeight(self):
        cl, ct, cr, cb = wgui.GetClientRect(self.hwnd)
        # TODO this is an approximation, not counting borders etc
        return self.getHeight() - (cb - ct)

    def purifyStyle(self):
        self.setStyle(self.getStyle() & ~(wc.WS_CAPTION))

    def getStyle(self):
        if not self.isAlive():
            print("Error, window went away!")
            return
        return wgui.GetWindowLong(self.hwnd, wc.GWL_STYLE)

    def preparePos(self, xy):
        self.op["pos"] = xy

    def prepareSize(self, wh):
        self.op["size"] = wh

    def prepareSetUnder(self, win):
        self.op["under"] = win

    def applyOps(self):
        if not self.isAlive():
            print("Error, window went away!")
            return

        flags = 0
        win = 0
        x, y, w, h = 0, 0, 0, 0

        if "under" in self.op:
            win = self.op["under"]
        else:
            flags |= wc.SWP_NOZORDER

        if "pos" in self.op:
            x, y = self.op["pos"]
        else:
            flags |= wc.SWP_NOMOVE

        if "size" in self.op:
            w, h = self.op["size"]
        else:
            flags |= wc.SWP_NOSIZE

        self.op = {}

        wgui.SetWindowPos(self.hwnd, win, x, y, w, h, flags)

    def setStyle(self, style):
        if not self.isAlive():
            print("Error, window went away!")
            return
        print "setStyle:", style
        wgui.SetWindowLong(self.hwnd, wc.GWL_STYLE, style)
        wgui.SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, 
                wc.SWP_NOMOVE | wc.SWP_NOSIZE | 
                wc.SWP_NOZORDER | wc.SWP_FRAMECHANGED )

    def doFocus(self):
        if not self.isAlive():
            print("Error, window went away!")
            return
        my_hwnd = native.getKeyOp().getHwndW32()

        # If called from a WM_HOTKEY event processor,
        # this should succeed (except for a few cases, like switching away
        # from a Start menu)
        wgui.SetForegroundWindow(my_hwnd)

        # Once the wm is the foreground, we can pass it over
        wgui.SetForegroundWindow(self.hwnd)

