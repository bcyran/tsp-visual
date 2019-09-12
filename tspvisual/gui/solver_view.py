import wx


class SolverView(wx.Panel):
    """Main view of the app, solver controls and tsp view.
    """

    def __init__(self, parent):
        super(SolverView, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Panel sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Solver controls and TSP view
        self.controls = SolverControls(self)
        self.tsp_view = TSPView(self)
        sizer.Add(self.controls, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.tsp_view, 1,
                  wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(sizer)


class SolverControls(wx.Panel):
    """Solver selection and controls.
    """

    def __init__(self, parent):
        super(SolverControls, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        pass


class TSPView(wx.Panel):
    """Visualisation of the TSP instance.
    """

    def __init__(self, parent):
        super(TSPView, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        pass
