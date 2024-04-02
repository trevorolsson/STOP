import wx
import wx.lib.activex
import numpy as np
import comtypes.client
from datetime import timedelta
 
from tools import *


class Page1(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        #%% Create spatial control space
        self.ltp = LTP(self, sizer)
        
        #%% create temporal control space
        self.lbp = LBP(self, sizer)
        
class LTP(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        pg1_tp_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Spatial" ), wx.VERTICAL )
        
        self.sbs_ltp = SBS_LTP(pg1_tp_sbSizer.GetStaticBox(), sizer)
        pg1_tp_sbSizer.Add( self.sbs_ltp, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( pg1_tp_sbSizer )
        self.Layout()
        pg1_tp_sbSizer.Fit( self )
        sizer.Add( self, 1, wx.EXPAND |wx.ALL, 5 )

class LBP(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        pg1_bm_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Temporal" ), wx.VERTICAL )
        
        self.sbs_lbp = SBS_LBP(pg1_bm_sbSizer.GetStaticBox(), sizer, pg1_bm_sbSizer)
        pg1_bm_sbSizer.Add( self.sbs_lbp, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( pg1_bm_sbSizer )
        self.Layout()
        pg1_bm_sbSizer.Fit( self )
        sizer.Add( self, 1, wx.EXPAND |wx.ALL, 5 )
    
    def isConnected(self, event):
        print('hello')
        return
        
class SBS_LTP(wx.Panel):
    def __init__(self, parent, sizer = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        pg1_tp_sbs_p_gSizer = wx.GridSizer( 1, 2, 0, 0 )
        
        spatial_define_bSizer = wx.BoxSizer( wx.VERTICAL )
        
        movement_toggleChoices = [ u"Jog", u"Relative" ]
        self.movement_toggle = wx.RadioBox( self, wx.ID_ANY, u"Movement Mode", wx.DefaultPosition, wx.DefaultSize, movement_toggleChoices, 1, wx.RA_SPECIFY_COLS )
        self.movement_toggle.SetSelection( 1 )
        spatial_define_bSizer.Add( self.movement_toggle, 0, wx.EXPAND, 5 )
        self.Bind(wx.EVT_RADIOBOX, self.onRadio, self.movement_toggle)
        
        
        
        define_stepsize_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Step Size" ), wx.VERTICAL )
        
        stepsize_gSizer = wx.GridSizer( 1, 2, 0, 0 )
        
        self.stepsize_set_button = wx.Button( define_stepsize_sbSizer.GetStaticBox(), wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
        stepsize_gSizer.Add( self.stepsize_set_button, 0, wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onSetStep, self.stepsize_set_button)
        
        self.stepsize_box = wx.SpinCtrl( define_stepsize_sbSizer.GetStaticBox(), wx.ID_ANY, style  =  wx.SP_ARROW_KEYS|wx.SP_WRAP, min = 0, max = 10, initial = 1 )
        stepsize_gSizer.Add( self.stepsize_box, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_SPINCTRL, self.onStepChange, self.stepsize_box)
        self.Step = self.stepsize_box.GetValue()
        
        define_stepsize_sbSizer.Add( stepsize_gSizer, 1, wx.EXPAND, 5 )
        
        
        spatial_define_bSizer.Add( define_stepsize_sbSizer, 1, wx.EXPAND, 5 )
        
        define_indicator_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"(x, y) Coordinates" ), wx.VERTICAL )
        
        indicator_gSizer = wx.GridSizer( 1, 2, 0, 0 )
        
        self.indicator_x = wx.TextCtrl( define_indicator_sbSizer.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT|wx.RAISED_BORDER )
        self.indicator_x.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
        self.indicator_x.Enable( False )
        
        indicator_gSizer.Add( self.indicator_x, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.indicator_y = wx.TextCtrl( define_indicator_sbSizer.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT|wx.RAISED_BORDER )
        self.indicator_y.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
        self.indicator_y.Enable( False )
        
        indicator_gSizer.Add( self.indicator_y, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        define_indicator_sbSizer.Add( indicator_gSizer, 1, wx.EXPAND, 5 )
        
        
        spatial_define_bSizer.Add( define_indicator_sbSizer, 1, wx.EXPAND, 5 )
        
        
        pg1_tp_sbs_p_gSizer.Add( spatial_define_bSizer, 1, wx.EXPAND, 5 )
        
        spatial_control_bSizer = wx.GridSizer( 3, 3, 0, 0 )
        
        
        # spatial_control_bSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.connect_indicator = wx.StaticBox( self, wx.ID_ANY, '', wx.DefaultPosition, size = (20,20), style = wx.EXPAND )
        spatial_control_bSizer.Add( self.connect_indicator, 0,  wx.ALIGN_CENTER, 0)
        self.connect_indicator.SetBackgroundColour(wx.Colour(225,0,0))
        self.connect_indicator.SetForegroundColour(wx.Colour(225,0,0))
        
        
        self.up_button = wx.Button( self, wx.ID_ANY, u"Up", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.up_button, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onUp, self.up_button)
        
        spatial_control_bSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.left_button = wx.Button( self, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.left_button, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onLeft, self.left_button)
        
        self.zero_button = wx.Button( self, wx.ID_ANY, u"ZERO", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.zero_button, 0, wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onZero, self.zero_button)
        
        self.right_button = wx.Button( self, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.right_button, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onRight, self.right_button)
        
        spatial_control_bSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.down_button = wx.Button( self, wx.ID_ANY, u"Down", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.down_button, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onDown, self.down_button)
        
        self.stop_button = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
        spatial_control_bSizer.Add( self.stop_button, 0, wx.ALL|wx.EXPAND, 5 )
        self.Bind(wx.EVT_BUTTON, self.onStop, self.stop_button)
        self.stop_button.SetBackgroundColour(wx.Colour( 225, 0, 0 ))
        self.stop_button.SetForegroundColour(wx.Colour( 225, 225, 225 ))
        
        pg1_tp_sbs_p_gSizer.Add( spatial_control_bSizer, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.SetSizer( pg1_tp_sbs_p_gSizer )
        self.Layout()
        pg1_tp_sbs_p_gSizer.Fit( self )

    
    
    def onRadio(self, event):
        last_val = self.Step
        if self.movement_toggle.GetSelection() == 0:
            self.stepsize_set_button.Enable( False )
            self.stepsize_box.Enable(False)
            self.stepsize_box.SetValue(0)
            pass
        elif self.movement_toggle.GetSelection() == 1:
            self.stepsize_set_button.Enable( True )
            self.stepsize_box.Enable(True)
            self.stepsize_box.SetValue(last_val)
            pass
        return

    def onStepChange(self, event):
        if self.Step != self.stepsize_box.GetValue():
            self.stepsize_set_button.SetBackgroundColour(wx.Colour( 0, 204, 0 ))
        else:
            pass
        return

    def onSetStep(self, event):
        step = self.stepsize_box.GetValue()
        self.Step = step
        self.stepsize_set_button.SetBackgroundColour(wx.Colour( 225, 225, 225 ))
        return
         
    def onZero(self, event):
        self.indicator_x.SetLabelText(f'{0}')
        self.indicator_y.SetLabelText(f'{0}')
        return
    
    def onUp(self, event):
        if self.movement_toggle.GetSelection() == 0:
            pass
        elif self.movement_toggle.GetSelection() == 1:
            step = self.Step
            if step != self.stepsize_box.GetValue():
                print('Ensure stepsize is confirmed')
            else:
                currY = int(self.indicator_y.GetLabelText())
                nextY = currY + step
                self.indicator_y.SetLabelText(str(nextY))
        return
    
    def onDown(self, event):
        if self.movement_toggle.GetSelection() == 0:
            pass
        elif self.movement_toggle.GetSelection() == 1:
            step = self.Step
            if step != self.stepsize_box.GetValue():
                print('Ensure stepsize is confirmed')
            else:
                currY = int(self.indicator_y.GetLabelText())
                nextY = currY - step
                self.indicator_y.SetLabelText(str(nextY))
        return
    
    def onLeft(self, event):
        if self.movement_toggle.GetSelection() == 0:
            pass
        elif self.movement_toggle.GetSelection() == 1:
            step = self.Step
            if step != self.stepsize_box.GetValue():
                print('Ensure stepsize is confirmed')
            else:
                currX = int(self.indicator_x.GetLabelText())
                nextX = currX - step
                self.indicator_x.SetLabelText(str(nextX))
        return
    
    def onRight(self, event):
        if self.movement_toggle.GetSelection() == 0:
            pass
        elif self.movement_toggle.GetSelection() == 1:
            step = self.Step
            if step != self.stepsize_box.GetValue():
                print('Ensure stepsize is confirmed')
            else:
                currX = int(self.indicator_x.GetLabelText())
                nextX = currX + step
                self.indicator_x.SetLabelText(str(nextX))
        return
    
    def onStop(self, event):
        print('Put stop action here')
        return

class SBS_LBP(wx.Panel):
    def __init__(self, parent, sizer = None, sizer2=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        pg1_bm_sbs_bSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.control_panel = wx.Panel( sizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        control_gSizer = wx.GridSizer( 1, 3, 0, 0 )
        
        self.connect_indicator = wx.StaticBox( self.control_panel, wx.ID_ANY, '', wx.DefaultPosition, size = (20,20), style = wx.EXPAND )
        control_gSizer.Add( self.connect_indicator, 0,  wx.ALIGN_CENTER, 5)
        self.connect_indicator.SetBackgroundColour(wx.Colour(225,0,0))
        self.connect_indicator.SetForegroundColour(wx.Colour(225,0,0))
        
        self.connect_button = wx.Button( self.control_panel, wx.ID_ANY, u"Initialize", wx.DefaultPosition, wx.DefaultSize, 0 )
        control_gSizer.Add( self.connect_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.connect_button.Bind(wx.EVT_BUTTON, self.onInitialize)
        
        self.stop_button = wx.Button( self.control_panel, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stop_button.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.stop_button.SetBackgroundColour( wx.Colour( 255, 0, 0 ) )
        self.stop_button.Bind(wx.EVT_BUTTON, self.onStop)
        
        control_gSizer.Add( self.stop_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        
        self.control_panel.SetSizer( control_gSizer )
        self.control_panel.Layout()
        control_gSizer.Fit( self.control_panel )
        pg1_bm_sbs_bSizer.Add( self.control_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.indicator_panel = wx.Panel( sizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        indicator_gSizer = wx.GridSizer( 1, 1, 0, 0 )
        
        self.stagepos_slider = FloatSlider(self.indicator_panel, -1, 1, 0., 25., 1e-4, style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        indicator_gSizer.Add( self.stagepos_slider, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.indicator_panel.SetSizer( indicator_gSizer )
        self.indicator_panel.Layout()
        indicator_gSizer.Fit( self.indicator_panel )
        pg1_bm_sbs_bSizer.Add( self.indicator_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.setting_panel = wx.Panel( sizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        setting_gSizer = wx.GridSizer( 1, 3, 0, 0 )
        
        velocity_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self.setting_panel, wx.ID_ANY, u"Velocity (mm/sec)" ), wx.VERTICAL )
        
        self.velocity_set = wx.TextCtrl( velocity_sbSizer.GetStaticBox(), wx.ID_ANY, u'0', wx.DefaultPosition, wx.DefaultSize, 0)
        velocity_sbSizer.Add( self.velocity_set, 0, wx.ALL, 5 )
        self.velocity_set.SetLabelText('0')
        setting_gSizer.Add( velocity_sbSizer, 1, wx.EXPAND, 5 )
        
        position_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self.setting_panel, wx.ID_ANY, u"Position (mm)" ), wx.VERTICAL )
        
        self.pos_set = wx.TextCtrl( position_sbSizer.GetStaticBox(), wx.ID_ANY, u'0', wx.DefaultPosition, wx.DefaultSize, 0)
        position_sbSizer.Add( self.pos_set, 0, wx.ALL, 5 )
        self.pos_set.SetLabelText('0')
        setting_gSizer.Add( position_sbSizer, 1, wx.EXPAND, 5 )
        
        go_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self.setting_panel, wx.ID_ANY, u"Start" ), wx.VERTICAL )
        
        self.go_button = wx.Button( go_sbSizer.GetStaticBox(), wx.ID_ANY, u"GO", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.go_button.SetBackgroundColour( wx.Colour( 0, 207, 0 ) )
        self.go_button.Bind(wx.EVT_BUTTON, self.onGo)
        
        go_sbSizer.Add( self.go_button, 0, wx.ALL, 5 )
        
        
        setting_gSizer.Add( go_sbSizer, 1, wx.EXPAND, 5 )
        
        
        self.setting_panel.SetSizer( setting_gSizer )
        self.setting_panel.Layout()
        setting_gSizer.Fit( self.setting_panel )
        pg1_bm_sbs_bSizer.Add( self.setting_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        
        sizer2.Add( pg1_bm_sbs_bSizer, 1, wx.EXPAND, 5 )
    
    def onInitialize(self, event):
        print('Initilize event goes here.')
        return
    
    def onStop(self, event):
        print('Stop event goes here.')
        return
       
    def onGo(self, event):
        vel = float(self.velocity_set.GetValue())
        pos = float(self.pos_set.GetValue())
        current = float(self.stagepos_slider.GetValue())
        delta = abs(current-pos)
        
        if vel == 0:
            print('Stage will not move.')
        else:
            print('This run will take {} seconds.'.format(timedelta(seconds=delta/vel)))
        return