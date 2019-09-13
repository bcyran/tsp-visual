from operator import itemgetter

import wx

from tspvisual.gui.helpers import borders


class SolverView(wx.Panel):
    """Main view of the app, solver controls and tsp view.
    """

    def __init__(self, parent):
        super(SolverView, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        # Panel sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Solver controls and TSP view
        self.controls = SolverControls(self)
        self.tsp_view = TSPView(self)
        sizer.Add(self.controls, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.tsp_view, 1, wx.EXPAND | borders('trb'), 10)

        self.SetSizer(sizer)

    def set_cities(self, cities):
        """Sets city list to display in TSPView.

        :param list cities: List of the cities coordiantes to display in
            normalized form (in [0, 1] range).
        """

        self.tsp_view.set_cities(cities)

    def reset(self):
        """Resets this control to its initial empty state.
        """

        self.tsp_view.reset()


class SolverControls(wx.Panel):
    """Solver selection and controls.
    """

    def __init__(self, parent):
        super(SolverControls, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        pass


class TSPView(wx.Panel):
    """Visualisation of the TSP instance.
    """

    PADDING = 20
    CITY_RADIUS = 2

    def __init__(self, parent):
        super(TSPView, self).__init__(parent)

        # Cities list
        self.cities = []
        self.points = []

        # GUI
        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        # Background style
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        # Event bindings
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_SIZE, self._on_resize)

    def _on_paint(self, event):
        """Paints currently set cities and paths.
        """

        # Create and clear drawing context
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

        # Skip if there are no points
        if not self.points:
            return

        # Define pen and brush
        dc.SetPen(wx.Pen('BLACK'))
        dc.SetBrush(wx.Brush('BLACK'))

        # Draw cities
        for c in self.points:
            dc.DrawCircle(c[0], c[1], self.CITY_RADIUS)

    def _on_resize(self, event):
        """Handles resize event.
        """

        self.calculate_points()

    def set_cities(self, cities):
        """Sets cities list, triggers point calculation and repaint.
        """

        self.cities = cities
        self.calculate_points()
        self.Refresh()

    def calculate_points(self):
        """Calculates positions of points representing cities.
        """

        # Skip if no cities are set
        if not self.cities:
            return

        # Clear current points
        self.points.clear()

        # Find max x and y value
        max_x = max(self.cities, key=itemgetter(0))[0]
        max_y = max(self.cities, key=itemgetter(1))[1]
        # Drawing area size
        w, h = self.GetClientSize()
        # Usable area
        uw, uh = w - self.PADDING * 2, h - self.PADDING * 2
        # Size of the drawing if it was scaled to fit the longer area side
        vw, vh = uw / max_x, uh / max_y
        # Shorter side
        side = min(vw, vh)
        # Effective padding
        exp, eyp = (w - side * max_x) / 2, (h - side * max_y) / 2

        # Calculate for all points
        for c in self.cities:
            x, y = c[0] * side + exp,  c[1] * side + eyp
            self.points.append((x, y))

    def reset(self):
        """Resets this control to its initial empty state.
        """

        self.cities = []
        self.points = []
        self.Refresh()
