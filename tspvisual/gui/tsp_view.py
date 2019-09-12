import wx


class TSPView(wx.Panel):

    def __init__(self, parent):
        super(TSPView, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Background color
        self.SetBackgroundColour('white')
