import wx
import wx.lib.inspection

from tspvisual.gui.solver_controls import SolverControls
from tspvisual.gui.tsp_view import TSPView


class App(wx.Frame):
    """Main app window wrapping around everything else.
    """

    def __init__(self):
        super(App, self).__init__(None, title='TSP Visual')
        self.init_ui()
        self.Show()
        self.SetSize(1200, 900)
        self.Centre()

    def init_ui(self):
        # Menubar
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        exit_mi = file_menu.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        inspect_mi = file_menu.Append(wx.ID_ANY, 'Debug', 'Debug GUI')
        menu_bar.Append(file_menu, 'File')
        self.SetMenuBar(menu_bar)

        # Main layout
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label='No instance loaded')
        title_font = wx.Font(wx.FontInfo(18))
        title.SetFont(title_font)
        title.SetMinSize(title.GetTextExtent(title.Label))
        sizer.Add(title, 0, wx.EXPAND | wx.ALL, 10)

        # Tabs
        notebook = wx.Notebook(panel)
        main_tab = MainTab(notebook)
        stats_tab = StatsTab(notebook)
        notebook.AddPage(main_tab, 'Main')
        notebook.AddPage(stats_tab, 'Stats')
        sizer.Add(notebook, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(sizer)
        panel.Layout()
        self.Layout()

        # Event bindings
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), exit_mi)
        self.Bind(wx.EVT_MENU, wx.lib.inspection.InspectionTool().Show,
                  inspect_mi)


class MainTab(wx.Panel):
    """Main tab of the app, solver controls and tsp view.
    """

    def __init__(self, parent):
        super(MainTab, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Background color
        self.SetBackgroundColour('whitesmoke')

        # Panel sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Solver controls and TSP view
        controls = SolverControls(self)
        tsp_view = TSPView(self)
        sizer.Add(controls, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(tsp_view, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(sizer)
        self.Layout()


class StatsTab(wx.Panel):
    """Second tab, graphs and statistics
    """

    def __init__(self, parent):
        super(StatsTab, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Background color
        self.SetBackgroundColour('whitesmoke')
