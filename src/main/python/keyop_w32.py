"""
Native key grabbing operations

"""
import pyHook
import win32api as wapi
import win32gui as wgui
import win32ui  as wui
import win32con as wc
import ctypes

import win_w32
from keyevent import KeyEvent

class Keyop:

    instance_ = None

    @classmethod
    def getInstance(cls):
        if cls.instance_ == None:
            cls.instance_ = Keyop()

        return cls.instance_

    def __init__(self):
        self.wm_hwnd = self.createWin_()
        print("Created win:", self.wm_hwnd)
        self.wm_wnd = wui.CreateWindowFromHandle(self.wm_hwnd)
        self.hotkeys = {} # id -> fun     

    def getHwndW32(self):
        return self.wm_hwnd

    def wndProc_(self, hwnd, msg, wp, lp):
        if msg == wc.WM_HOTKEY:
            print("hotkey:", hwnd, msg, wp, lp)
            self.hotkeys[int(wp)]()
            return 0

        elif msg == wc.WM_DESTROY:
            print("destroy")
            wapi.PostQuitMessage(0)
            return 0

        return wgui.DefWindowProc(hwnd, msg, wp, lp) 


    def createWin_(self):
        hinst = wapi.GetModuleHandle(None)
        cls = wgui.WNDCLASS()
        cls.hInstance = hinst
        cls.lpszClassName = "ciccwm_cls"
        cls.lpfnWndProc = self.wndProc_
        cls.style = wc.CS_GLOBALCLASS | wc.CS_VREDRAW | wc.CS_HREDRAW
        cls.hbrBackground = wc.COLOR_WINDOW + 1
        cls.hCursor = wgui.LoadCursor(0, wc.IDC_ARROW)
        
        clsa = wgui.RegisterClass(cls)

        l, t, b, r = 10, 10, 30, 30

        hwnd = wgui.CreateWindow(clsa, "ciccwm",
                wc.WS_CAPTION | wc.WS_VISIBLE | wc.WS_SYSMENU,
                l, t, b, r, 0, 0, hinst, None)

        wgui.ShowWindow(hwnd, False) # hide win
        wgui.UpdateWindow(hwnd)

        return hwnd

    def setUserKeyListener(self, userKeyListener):
        """
        userKeyListener: KeyEvent -> Bool

        The userKeyListener should decide if the key is intended for
        the WM and quickly return. Processing operation should be
        dispatched via a queue.

        """
        self.userKeyListener = userKeyListener

    def addHotkeyListener(self, cbFun, forCode, 
            withAlt=False, withCtrl=False, withShift=False, withWin=False):

        print("addHotkeyListener", forCode)

        hid = 1
        if len(self.hotkeys) != 0:
            hid += max(self.hotkeys)

        mods = 0
        if withAlt:     mods |= wc.MOD_ALT
        if withCtrl:    mods |= wc.MOD_CONTROL
        if withShift:   mods |= wc.MOD_SHIFT
        if withWin:     mods |= wc.MOD_WIN

        self.hotkeys[hid] = cbFun

        print("hwnd", self.wm_hwnd)
        print("wnd", self.wm_wnd)
        print("hid", hid)
        print("mods", mods)
        print("forCode", forCode)
        ret = ctypes.windll.user32.RegisterHotKey(self.wm_hwnd, hid, mods, forCode)
        print("setHotkeyListener", forCode, ret)

    def hotkeyListener_(self, msg):
        print("Hotkey received:", msg)

    def startEvents(self):
        print("startEvents")
        self.hookManager = pyHook.HookManager()
        self.hookManager.KeyAll = self.keyListener_
        self.hookManager.HookKeyboard()

        print("start pumping")
        wgui.PumpMessages()
        print("finished pumping")

    def stopEvents(self):
        print("stopEvents")
        self.wm_wnd.DestroyWindow()
        self.hookManager.UnhookKeyboard()
    
    def keyListener_(self, event):
        keyId       = event.KeyID
        forWindow   = win_w32.Window(event.Window)
        isPress     = event.Transition == 0

        def getState(vkey):
            id = pyHook.HookConstants.VKeyToID(vkey)
            st = pyHook.GetKeyState(id)
            return st

        withAlt     = getState('VK_MENU')       != 0 # ?
        withCtrl    = getState('VK_CONTROL')    != 0
        withShift   = getState('VK_SHIFT')      != 0
        
        kEvent = KeyEvent(keyId, forWindow, isPress, withAlt, withCtrl, withShift)

        if self.userKeyListener is not None:
            return self.userKeyListener(kEvent)
        
        return True # allow key

