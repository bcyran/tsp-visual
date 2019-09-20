from enum import Enum
from operator import itemgetter

import wx
import wx.propgrid as wxpg
from pubsub import pub

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

        # Currently selected solver and tsp
        self.solver = None
        self.tsp = None

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
        props_box_sizer.Add(self.solver_properties, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)

        # Event bindings
        self.solver_select.Bind(wx.EVT_CHOICE, self._on_select)
        pub.subscribe(self._on_solver_change, 'SOLVER_CHANGE')
        pub.subscribe(self._on_tsp_change, 'TSP_CHANGE')

        # Run solver selection event handler to create default solver
        self._on_select(None)

    def _on_select(self, event):
        """Handles selecting solver from solvers combobox.
        """

        solver_name = self.solver_names[self.solver_select.GetSelection()]
        solver_class = self.solvers[solver_name]
        solver = solver_class()

        pub.sendMessage('SOLVER_CHANGE', solver=solver)

    def _on_solver_change(self, solver):
        """Handles solver change event.
        """

        self.solver = solver

    def _on_tsp_change(self, tsp):
        """Handles TSP change event.
        """

        self.tsp = tsp


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
        pub.subscribe(self._on_tsp_change, 'TSP_CHANGE')

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

    def _on_tsp_change(self, tsp):
        """Handles TSP change event.
        """

        self.reset()

        if not tsp:
            return

        if not tsp.display:
            wx.MessageBox('This instance does not have display data',
                          'Warning', wx.OK | wx.ICON_WARNING)
            return

        self.set_cities(tsp.display)

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


class SolverProperties(wx.propgrid.PropertyGrid):
    """Panel for configuring solver-specific options.
    """

    def __init__(self, parent):
        super(SolverProperties, self).__init__(parent,
                                               style=wxpg.PG_HIDE_MARGIN |
                                               wxpg.PG_BOLD_MODIFIED |
                                               wxpg.PG_TOOLTIPS)

        # Currently selected solver
        self.solver = None

        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        # Event bindings
        self.Bind(wxpg.EVT_PG_CHANGED, self._on_changed)
        pub.subscribe(self._on_solver_change, 'SOLVER_CHANGE')

    def _on_changed(self, event):
        """Applies current properties values to the currently set solver.
        """

        for prop in self.Properties:
            solver_prop = prop.GetAttribute('solver_property')
            value = solver_prop.type(prop.GetValue())
            setattr(self.solver, solver_prop.field, value)

    def _on_solver_change(self, solver):
        """Handles solver change event.
        """

        self.set_solver(solver)

    def set_solver(self, solver):
        """Sets current solver and builds UI basing on its properties.

        :param Solver solver: Solver to show properties of.
        """

        # Set the solver
        self.solver = solver

        # Reset the properties
        self.reset()

        # Skip if there is no solver or solver has no properties
        if not self.solver or not self.solver.properties:
            return

        # For each property
        for p in self.solver.properties:
            # Create property object with appropriate type
            if p.type is int:
                prop = wxpg.IntProperty()
            elif p.type is float:
                prop = wxpg.FloatProperty()
            elif issubclass(p.type, Enum):
                prop = wxpg.EnumProperty()
                labels = list(map(lambda c: c.name, p.type))
                values = list(map(lambda c: c.value, p.type))
                prop_choices = wxpg.PGChoices(labels=labels, values=values)
                prop.SetChoices(prop_choices)

            # Set label and value
            prop.SetLabel(p.name)
            prop.SetValue(p.default)
            prop.SetDefaultValue(p.default)
            prop.SetAttribute('solver_property', p)

            # And append the property object
            self.Append(prop)

        # Fit columns and layout the parent
        self.FitColumns()
        self.GetParent().Layout()

    def reset(self):
        """Resets control to initial state.
        """

        self.Clear()
