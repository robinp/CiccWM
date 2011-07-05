"""
Native window operations

"""
import win32api as wapi
import win32gui as wgui
import win32con as wc

class Winop:

    instance_ = None

    @classmethod
    def getInstance(cls):
        if cls.instance_ == None:
            cls.instance_ = Winop()

        return cls.instance_

    def __init__(self):
        pass

    def getScreenSize(self):
        w = wapi.GetSystemMetrics(wc.SM_CXFULLSCREEN)
        h = wapi.GetSystemMetrics(wc.SM_CYFULLSCREEN)

        BUFFER = 0

        return (w, h - BUFFER)


