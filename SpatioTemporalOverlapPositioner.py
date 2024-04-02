import wx
import wx.lib.activex
import numpy as np
import comtypes.client
from datetime import timedelta
# import wx.xrc

from tab1 import *
from tab2 import *
from tab3 import *



class EventSink(object):
    def __init__(self, frame):
        self.counter = 0
        self.frame = frame
    
    def DataReady(self):
        counter += 1
        self.frame.title = f"DataReady fired {self.counter} times"

class LMP(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.gd = wx.lib.activex.ActiveXCtrl(parent = self,
                                             size = (0,0),
                                             axID = 'DATARAYOCX.GetDataCtrl.1')
        
        # Get location of geometric center of peak
        # self.cent_x, self.cent_y = self.gd.ctrl.GetCentroidXlocation(), self.gd.ctrl.GetCentroidYlocation() 

        parent.Show()
        
        sink = EventSink(self)
        self.sink = comtypes.client.GetEvents(self.gd.ctrl,sink)
        
        connection_i = wx.lib.activex.ActiveXCtrl(parent = self, 
                                        size=(75,25), 
                                        pos=(10, 10),
                                        axID='DATARAYOCX.ButtonCtrl.1')
        connection_i.ctrl.ButtonID = 297 # Green camera indicator

        # Creates the ccd image to show profile
        self.ccd = wx.lib.activex.ActiveXCtrl(parent = self,
                                         size = (337, 297),
                                         pos = (10,10),
                                         axID = 'DATARAYOCX.CCDimageCtrl.1')
        
        # Crosshair Controls
        self.gd.ctrl.ForceCrosshairsToZero()
        self.gd.ctrl.AutoSnap = 3
        self.Bind(wx.EVT_CHAR_HOOK, self.onNudge)
        
        self.exp = wx.lib.activex.ActiveXCtrl(parent=self,
                                             size=(169,20),
                                             pos=(10,320),
                                             axID='DATARAYOCX.ButtonCtrl.1')
        self.exp.ctrl.ButtonID = 412
        
        self.exp = wx.lib.activex.ActiveXCtrl(parent=self,
                                              size=(169,20),
                                              pos=(178,320),
                                              axID='DATARAYOCX.ButtonCtrl.1')
        self.exp.ctrl.ButtonID = 421
        
        self.exp = wx.lib.activex.ActiveXCtrl(parent=self,
                                              size=(169,20),
                                              pos=(178,340),
                                              axID='DATARAYOCX.ButtonCtrl.1')
        self.exp.ctrl.ButtonID = 301
        
        # Creates an intensity profile from either axis of the crosshairs
        self.px = wx.lib.activex.ActiveXCtrl(parent=self,
                                             size=(169,155),
                                             pos=(10,340),
                                            axID='DATARAYOCX.ProfilesCtrl.1')
        self.px.ctrl.ProfileID=22 # Profile plot x-axis
        self.x_data = np.array(self.px.ctrl.GetProfileDataAsVariant())
        
        
        self.py = wx.lib.activex.ActiveXCtrl(parent=self,
                                             size=(169,155),
                                             pos=(178,340),
                                             axID='DATARAYOCX.ProfilesCtrl.1')
        self.py.ctrl.ProfileID = 23 # Profile plot y-axis
        self.y_data = np.array(self.py.ctrl.GetProfileDataAsVariant())
                             
        self.gd.ctrl.StartDriver()                      
    
    def onNudge(self, event):
        if event.GetKeyCode() == wx.WXK_UP:
            self.gd.ctrl.NudgeCrosshairs(1, 1)
        if event.GetKeyCode() == wx.WXK_DOWN:
            self.gd.ctrl.NudgeCrosshairs(1, -1)
        if event.GetKeyCode() == wx.WXK_LEFT:
            self.gd.ctrl.NudgeCrosshairs(0, -1)
        if event.GetKeyCode() == wx.WXK_RIGHT:
            self.gd.ctrl.NudgeCrosshairs(0, 1)
        else:
            event.Skip()
            
class RMP(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__( self, parent)
        
        #%% Set Page 1 Format
        pg1_bSizer = wx.BoxSizer( wx.VERTICAL )
        self.page1 = Page1(self, pg1_bSizer)
        self.page1.SetSizer( pg1_bSizer )
        self.page1.Layout()
        pg1_bSizer.Fit( self.page1 )
        self.AddPage( self.page1, u"Position", True )
        #%% Add Page 2
        pg2_bSizer = wx.GridSizer( 1, 2, 0, 0)
        self.page2 = Page2(self, pg2_bSizer)
        self.AddPage( self.page2, u"Inspect", False )
        #%% Add page 3
        self.page3 = Page3(self)
        self.AddPage( self.page3, u"Scan", False )

class main_frame( wx.Frame ):
    
    def __init__( self ):
        wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = u"SpatioTemporal Overlap Positioner", pos = wx.DefaultPosition, size = wx.Size( 750,550 ), style = wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^ wx.MAXIMIZE_BOX|wx.TAB_TRAVERSAL )
        self.create_menu()
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        main_gSizer = wx.GridSizer( 1, 2, 0, 0 )
        
        #%% Add main left panel
        self.lmp = LMP(self)
        main_gSizer.Add( self.lmp, 1, wx.EXPAND |wx.ALL, 5 ) 
        #%% Add main right panel (notebook format)
        self.rmp = RMP(self)
        main_gSizer.Add( self.rmp, 1, wx.EXPAND |wx.ALL, 5 )
        #%% Set master sizer for entire window
        self.SetSizer( main_gSizer )
        self.Layout()
        self.Centre( wx.BOTH )
  
    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        save_prompt = menu_file.Append(-1, 'Save Profile\tCtrl-S', 'Save settings to file')
        self.Bind(wx.EVT_MENU, None, save_prompt)
        
        import_prompt = menu_file.Append(-1, 'Import Profile\tCtrl-I', 'Import settings from file')
        self.Bind(wx.EVT_MENU, None, import_prompt)
        menu_file.AppendSeparator()
        
        exit_prompt = menu_file.Append(-1, 'Exit\tAlt-F4', 'Exit the application')
        self.Bind(wx.EVT_MENU, self.on_exit, exit_prompt)
        
        about_file = wx.Menu()
        about_prompt = about_file.Append(-1, 'About\tCtrl-H')
        self.Bind(wx.EVT_MENU, None, about_prompt)
        
        self.menubar.Append(menu_file, 'File')
        self.menubar.Append(about_file, 'About')
        
        self.SetMenuBar(self.menubar)
        
    def __del__( self ):
        pass
    
    def on_exit(self, event):
         self.Destroy()
         
if __name__  == '__main__':
    app = wx.App()
    main_frame().Show()
    app.MainLoop()
