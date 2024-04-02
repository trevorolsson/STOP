import wx
import wxmplot as wm
import wxmplot.interactive as wi
import numpy as np
 
class Page2(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ltp = LTP(self, sizer)
        
class LTP(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        pg1_tp_sbSizer = wx.BoxSizer( wx.VERTICAL )
        
        

        
        
        #self.sbs_ltp = SBS_LTP(pg1_tp_sbSizer.GetStaticBox(), sizer)
        #pg1_tp_sbSizer.Add( self.sbs_ltp, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( pg1_tp_sbSizer )
        self.Layout()
        pg1_tp_sbSizer.Fit( self )
        sizer.Add( self, 1, wx.EXPAND |wx.ALL, 5 )

class LBP(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        pg1_bm_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Temporal" ), wx.VERTICAL )
        
        #self.sbs_lbp = SBS_LBP(pg1_bm_sbSizer.GetStaticBox(), sizer, pg1_bm_sbSizer)
        #pg1_bm_sbSizer.Add( self.sbs_lbp, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( pg1_bm_sbSizer )
        self.Layout()
        pg1_bm_sbSizer.Fit( self )
        sizer.Add( self, 1, wx.EXPAND |wx.ALL, 5 )
        
