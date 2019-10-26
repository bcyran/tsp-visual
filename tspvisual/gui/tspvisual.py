import wx
import wx.adv
import wx.lib.inspection
from pubsub import pub

from tspvisual.gui.export import export_results
from tspvisual.gui.helpers import borders
from tspvisual.gui.solver_stats import SolverStats
from tspvisual.gui.solver_view import SolverView
from tspvisual.gui.tsp_info import TSPInfo
from tspvisual.tsp import TSP


class TSPVisual(wx.Frame):
    """Main app window wrapping around everything else.
    """

    DEFAULT_TITLE = 'No instance loaded'

    def __init__(self):
        super(TSPVisual, self).__init__(None, title='TSP Visual')

        # Solver results (for exporting)
        self.results = None

        # GUI
        self._init_ui()
        self.Show()
        self.SetSize(1200, 900)
        self.Centre()

    def _init_ui(self):
        """Builds GUI.
        """

        # Menubar
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_mi = file_menu.Append(wx.ID_OPEN, 'Open', 'Open instance.')
        close_mi = file_menu.Append(wx.ID_CLOSE, 'Close', 'Close instance.')
        file_menu.AppendSeparator()
        exit_mi = file_menu.Append(wx.ID_EXIT, 'Exit', 'Exit application.')
        data_menu = wx.Menu()
        export_data_mi = data_menu.Append(wx.ID_ANY, 'Export data',
                                          'Export current solver data.')
        help_menu = wx.Menu()
        about_mi = help_menu.Append(wx.ID_ANY, 'About', 'About this program.')
        menu_bar.Append(file_menu, 'File')
        menu_bar.Append(data_menu, 'Data')
        menu_bar.Append(help_menu, 'Help')
        self.SetMenuBar(menu_bar)

        # Main layout
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        self.title = wx.StaticText(panel, label=self.DEFAULT_TITLE)
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
        sizer.Add(notebook, 1, wx.EXPAND | borders('lrb'), 10)

        panel.SetSizer(sizer)
        panel.Layout()
        self.Layout()

        # Event bindings
        self.Bind(wx.EVT_MENU, self._on_open, open_mi)
        self.Bind(wx.EVT_MENU, self._on_close, close_mi)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), exit_mi)
        self.Bind(wx.EVT_MENU, self._on_data_export, export_data_mi)
        self.Bind(wx.EVT_MENU, self._on_about, about_mi)
        pub.subscribe(self._on_tsp_change, 'TSP_CHANGE')
        pub.subscribe(self._on_solver_state_end, 'SOLVER_STATE_END')

    def _on_open(self, event):
        """Handles file opening.
        """

        # Present file picker and try to load selected instance
        with (wx.FileDialog(self, 'Open tsp instance.',
              wildcard='*.tsp',
              style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file = file_dialog.GetPath()

            try:
                tsp = TSP(file)
                pub.sendMessage('TSP_CHANGE', tsp=tsp)
            except Exception as e:
                wx.MessageBox(str(e), 'Error', wx.ICON_ERROR | wx.OK)

    def _on_close(self, event):
        """Handles file closing.
        """

        pub.sendMessage('TSP_CHANGE', tsp=None)

    def _on_data_export(self, event):
        """Handles data export.
        """

        # Show error and return if there is no results
        if not self.results:
            wx.MessageBox('No data to export.', 'Error', wx.ICON_ERROR | wx.OK)
            return

        # Present file picker and try to load selected instance
        with (wx.FileDialog(self, 'Save solver data.',
              wildcard='*.csv',
              style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file = file_dialog.GetPath()
            try:
                export_results(file, self.results)
                wx.MessageBox('Data exported successfully.', 'Success',
                              wx.ICON_INFORMATION | wx.OK)
            except Exception as e:
                wx.MessageBox(str(e), 'Error', wx.ICON_ERROR | wx.OK)

    def _on_about(self, event):
        """Shows about program box when.
        """

        desccription = 'TSP Visual is a program visualising TSP instances ' \
                       'and process of solving them for educational purposes.'

        license = 'No license for now.'

        about = wx.adv.AboutDialogInfo()
        about.SetName('TSP Visual')
        about.SetVersion('0.1')
        about.SetDescription(desccription)
        about.SetCopyright('(C) 2019 Bazyli Cyran')
        about.SetWebSite('https://bazylicyran.pl/')
        about.SetLicense(license)
        about.AddDeveloper('Bazyli Cyran')
        about.AddDocWriter('Bazyli Cyran')

        wx.adv.AboutBox(about)

    def _on_tsp_change(self, tsp):
        """Handles TSP change event.
        """

        if not tsp:
            self.title.SetLabel(self.DEFAULT_TITLE)
        else:
            self.title.SetLabel(f'Instance: {tsp.name}')

    def _on_solver_state_end(self, results):
        """Handles end of solving and stores reference to the results for
        future exporting.
        """

        self.results = results
