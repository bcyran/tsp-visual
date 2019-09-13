import wx


class TSPInfo(wx.Panel):
    """Displays specification of the TSP instance.
    """

    def __init__(self, parent):
        super(TSPInfo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Builds GUI.
        """

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Specification table
        self.table = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.table.InsertColumn(0, 'Key')
        self.table.InsertColumn(1, 'Value')
        sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)

    def set_specification(self, specification):
        """Populates table with given specification.
        """

        self.reset()

        for key, value in specification.items():
            self.table.Append((key, value))

        self.table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.table.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def reset(self):
        """Resets this panel to empty state.
        """

        self.specification = {}
        self.table.DeleteAllItems()
