import wx

from tspvisual.gui.tspvisual import TSPVisual


def main():
    app = wx.App()
    TSPVisual()
    app.MainLoop()


if __name__ == '__main__':
    main()
