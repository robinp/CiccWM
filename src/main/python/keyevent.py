class KeyEvent:

    def __init__(self, keyId, forWindow, isPress, withAlt, withCtrl, withShift):
        self.keyId      = keyId
        self.forWindow  = forWindow
        self.isPress    = isPress
        self.withAlt    = withAlt
        self.withCtrl   = withCtrl
        self.withShift  = withShift

