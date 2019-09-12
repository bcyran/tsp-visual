import wx
import wx.lib.inspection

from tspvisual.gui.solver_stats import SolverStats
from tspvisual.gui.solver_view import SolverView
from tspvisual.gui.tsp_info import TSPInfo
from tspvisual.tsp import TSP


class TSPVisual(wx.Frame):
    """Main app window wrapping around everything else.
    """

    def __init__(self):
        super(TSPVisual, self).__init__(None, title='TSP Visual')
        self.init_ui()
        self.Show()
        self.SetSize(1200, 900)
        self.Centre()

        # Current TSP instance
        self.tsp = None

    def init_ui(self):
        # Menubar
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_mi = file_menu.Append(wx.ID_OPEN, 'Open', 'Open tsp instance')
        file_menu.AppendSeparator()
        inspect_mi = file_menu.Append(wx.ID_ANY, 'Debug', 'Debug GUI')
        exit_mi = file_menu.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        help_menu = wx.Menu()
        about_mi = help_menu.Append(wx.ID_ANY, 'About', 'About this program')
        menu_bar.Append(file_menu, 'File')
        menu_bar.Append(help_menu, 'Help')
        self.SetMenuBar(menu_bar)

        # Main layout
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        self.title = wx.StaticText(panel, label='No instance loaded')
        self.title_font = wx.Font(wx.FontInfo(18))
        self.title.SetFont(self.title_font)
        self.title.SetMinSize(self.title.GetTextExtent(self.title.Label))
        sizer.Add(self.title, 0, wx.EXPAND | wx.ALL, 10)

        # Tabs
        notebook = wx.Notebook(panel)
        self.solver_view = SolverView(notebook)
        self.solver_stats = SolverStats(notebook)
        self.tsp_info = TSPInfo(notebook)
        notebook.AddPage(self.solver_view, 'Solver')
        notebook.AddPage(self.solver_stats, 'Stats')
        notebook.AddPage(self.tsp_info, 'Info')
        sizer.Add(notebook, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(sizer)
        panel.Layout()
        self.Layout()

        # Event bindings
        self.Bind(wx.EVT_MENU, self.on_open, open_mi)
        self.Bind(wx.EVT_MENU, wx.lib.inspection.InspectionTool().Show,
                  inspect_mi)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), exit_mi)
        self.Bind(wx.EVT_MENU, self.on_about, about_mi)

    def on_open(self, e):
        """File opening handler.
        """

        with (wx.FileDialog(self, 'Open tsp instance.',
              wildcard='*.tsp',
              style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file = file_dialog.GetPath()

            self.tsp = TSP(file)
            self.title.SetLabel(f'Instance: {self.tsp.name}')
            self.tsp_info.set_specification(self.tsp.specification)

    def on_about(self, e):
        pass
