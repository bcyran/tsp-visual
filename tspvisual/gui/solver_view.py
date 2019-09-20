from operator import itemgetter

import wx
import wx.lib.scrolledpanel

from tspvisual.gui.helpers import borders
from tspvisual.solver import Solver
from tspvisual.solvers import *  # noqa: F403, F401


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
        tsp_view_box = wx.StaticBox(self, label='Visualisation')
        tsp_view_box_sizer = wx.StaticBoxSizer(tsp_view_box)
        self.tsp_view = TSPView(tsp_view_box)
        tsp_view_box_sizer.Add(self.tsp_view, 1, wx.EXPAND)
        sizer.Add(self.controls, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(tsp_view_box_sizer, 1, wx.EXPAND | borders('trb'), 10)

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

        # List of all available solvers
        self.solvers = {s.name: s for s in Solver.__subclasses__()}
        self.solver_names = sorted(list(self.solvers.keys()))

        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        # Static boxes
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Solver box
        solver_box = wx.StaticBox(self, label='Solver selection')
        solver_box_sizer = wx.StaticBoxSizer(solver_box)
        sizer.Add(solver_box_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        # Result box
        res_box = wx.StaticBox(self, label='Result')
        res_box_sizer = wx.StaticBoxSizer(res_box)
        sizer.Add(res_box_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        # Properties box
        props_box = wx.StaticBox(self, label='Solver Properties')
        props_box_sizer = wx.StaticBoxSizer(props_box)
        sizer.Add(props_box_sizer, 1, wx.EXPAND)

        # Solver box contents
        solver_sizer = wx.GridBagSizer(10, 10)
        self.solver_select = wx.Choice(solver_box, choices=self.solver_names)
        self.solver_select.SetSelection(0)
        solver_sizer.Add(self.solver_select, (0, 0), (1, 2),
                         wx.EXPAND | borders('trl'), 10)
        self.solve_button = wx.Button(solver_box, label='Solve')
        solver_sizer.Add(self.solve_button, (1, 0), (1, 1),
                         wx.EXPAND | borders('lb'), 10)
        self.reset_button = wx.Button(solver_box, label='Reset')
        solver_sizer.Add(self.reset_button, (1, 1), (1, 1),
                         wx.EXPAND | borders('rb'), 10)
        solver_box_sizer.Add(solver_sizer)

        # Result box contents
        # No idea why this panel and sizer are necessary but this was the only
        # way to avoid GTK warnings
        result_panel = wx.Panel(self)
        result_sizer = wx.BoxSizer()
        self.result = wx.StaticText(result_panel, label='N/A',
                                    style=wx.ALIGN_CENTRE_HORIZONTAL)
        result_font = wx.Font(wx.FontInfo(16))
        self.result.SetFont(result_font)
        result_sizer.Add(self.result, 1, wx.ALL, 10)
        result_panel.SetSizer(result_sizer)
        res_box_sizer.Add(result_panel, 1)

        # Properties box contents
        self.solver_properties = SolverProperties(self)
        self.solver_properties.SetupScrolling()
        self.solver_properties.set_solver(self.solvers['Tabu Search'])
        props_box_sizer.Add(self.solver_properties, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)


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
        dc.SetPen(wx.Pen('black'))
        dc.SetBrush(wx.Brush('black'))

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
        uw, uh = (w - self.PADDING * 2), (h - self.PADDING * 2)
        # Size of the drawing if it was scaled to fit the longer area side
        vw, vh = (uw / max_x), (uh / max_y)
        # Shorter side
        side = min(vw, vh)
        # Effective padding
        exp, eyp = ((w - side * max_x) / 2), ((h - side * max_y) / 2)

        # Calculate for all points
        for c in self.cities:
            # Note the inverted y axis
            x, y = (c[0] * side + exp),  (h - (c[1] * side + eyp))
            self.points.append((x, y))

    def reset(self):
        """Resets this control to its initial empty state.
        """

        self.cities = []
        self.points = []
        self.Refresh()


class SolverProperties(wx.lib.scrolledpanel.ScrolledPanel):
    """Panel for configuring solver-specific options.
    """

    def __init__(self, parent):
        super(SolverProperties, self).__init__(parent)

        # Currently set solver
        self.solver = None

        self._init_ui()

    def _init_ui(self):
        """Builds GUI basing on current set solver.
        """

        # Skip if there is no solver or solver has no properties
        if not self.solver or not self.solver.properties:
            return

        sizer = wx.GridBagSizer(10, 10)

        self.SetSizer(sizer)

    def set_solver(self, solver):
        """Sets current solver and builds UI basing on its properties.

        :param Solver solver: Solver to show properties of.
        """

        self.solver = solver
        self._init_ui()

    def apply_properties(self):
        """Applies entered properties to the currently set solver.
        """

        pass
