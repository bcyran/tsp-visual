import wx
from pubsub import pub
from wx.lib.plot import PlotCanvas, PlotGraphics, PolyLine


class SolverStats(wx.Panel):
    """Displays solver statistics.
    """

    def __init__(self, parent):
        super(SolverStats, self).__init__(parent)

        # Solver states to plot
        self.results = []

        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.best_canvas = PlotCanvas(self)
        self.best_canvas.useScientificNotation = True
        self.current_canvas = PlotCanvas(self)
        self.current_canvas.useScientificNotation = True
        sizer.Add(self.best_canvas, 1, wx.EXPAND)
        sizer.Add(self.current_canvas, 1, wx.EXPAND)
        self._plot()

        self.SetSizer(sizer)

        pub.subscribe(self._on_solver_state_end, 'SOLVER_STATE_END')

    def _plot(self):
        """Plots best and current paths data.
        """

        self.best_canvas.Clear()
        best_points = [(r.time, r.best.distance) for r in self.results
                       if r.best is not None]
        best_line = PolyLine(best_points)
        best_plot = PlotGraphics([best_line], title='Best path',
                                 xLabel='Time [ns]', yLabel='Distance')
        self.best_canvas.Draw(best_plot)

        self.current_canvas.Clear()
        current_points = [(r.time, r.current.distance) for r in self.results
                          if r.current is not None]
        current_line = PolyLine(current_points)
        current_plot = PlotGraphics([current_line], title='Current path',
                                    xLabel='Time [ns]', yLabel='Distance')
        self.current_canvas.Draw(current_plot)

    def _on_solver_state_end(self, results):
        """Handles end of solving message.
        """

        self.results = results
        self._plot()
