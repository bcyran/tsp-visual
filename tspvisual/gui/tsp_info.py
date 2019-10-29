import wx
from pubsub import pub

from tspvisual.gui.helpers import borders


class TSPInfo(wx.Panel):
    """Displays specification of the TSP instance.
    """

    def __init__(self, parent):
        super(TSPInfo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        sizer = wx.BoxSizer(wx.VERTICAL)

        # TSP specification label
        tsp_label = wx.StaticText(self, label='TSP instance')
        sizer.Add(tsp_label, 0, wx.EXPAND | borders('tlr'), 10)
        # TSP specification table
        self.tsp_table = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.tsp_table.InsertColumn(0, 'Key')
        self.tsp_table.InsertColumn(1, 'Value')
        sizer.Add(self.tsp_table, 1, wx.EXPAND | borders('lr'), 10)

        # Separator line
        separator = wx.StaticLine(self)
        sizer.Add(separator, 0, wx.EXPAND | borders('trbl'), 10)

        # Tour specification label
        tour_label = wx.StaticText(self, label='Optimal tour')
        sizer.Add(tour_label, 0, wx.EXPAND | borders('lr'), 10)
        # Tour specification table
        self.tour_table = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.tour_table.InsertColumn(0, 'Key')
        self.tour_table.InsertColumn(1, 'Key')
        sizer.Add(self.tour_table, 1, wx.EXPAND | borders('lr'), 10)

        self.SetSizer(sizer)

        pub.subscribe(self._on_tsp_change, 'TSP_CHANGE')

    def _on_tsp_change(self, tsp):
        """Populates table with given specification.
        """

        self.reset()

        if not tsp:
            return

        for key, value in tsp.specification.items():
            self.tsp_table.Append((key, value))

        if tsp.opt_tour:
            for key, value in tsp.opt_tour.specification.items():
                self.tour_table.Append((key, value))

            self.tour_table.Append(('TOUR', str(tsp.opt_tour.tour)))
            self.tour_table.Append(('DISTANCE', str(tsp.opt_path.distance)))

        # Not pretty but forces first columns of both tables to be of equal
        # width
        self.tsp_table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.tour_table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        width1 = self.tsp_table.GetColumnWidth(0)
        width2 = self.tour_table.GetColumnWidth(0)
        max_width = max([width1, width2])
        self.tsp_table.SetColumnWidth(0, max_width)
        self.tour_table.SetColumnWidth(0, max_width)
        self.tsp_table.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.tour_table.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def reset(self):
        """Resets this panel to empty state.
        """

        self.specification = {}
        self.tsp_table.DeleteAllItems()
        self.tour_table.DeleteAllItems()
