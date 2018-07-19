#!python3
#coding: utf-8
"""
@author: yanbin
Any suggestion? Please contract yanbin_c@hotmail.com
"""
import  os
import  wx
import sys
import time,datetime
import numpy as np
import math
from time import clock
from threading import Thread
from scipy.special import erfcinv
from wx.lib.embeddedimage import PyEmbeddedImage

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'RMS to Eye-closure Jitter Calculator V0.1',size=(600,400))
        nb_main=wx.Notebook(self,-1,pos=(0,0),size=(600,400),style=wx.BK_DEFAULT)
        self.panel_c=panel_Calculator(nb_main,-1)
        self.panel_r=panel_ref(nb_main,-1)
        self.panel_v=panel_version(nb_main,-1)
        nb_main.AddPage(self.panel_c,"Jitter Cal")
        nb_main.AddPage(self.panel_r,"Ref Table")
        nb_main.AddPage(self.panel_v,"Version")
        self.panel_c.btn_run.Bind(wx.EVT_BUTTON,self.On_Run)
        
    def On_Run(self, event): 
        thread = Thread(target = self.On_Run_cal, args = (), name = self.On_Run_cal.__name__)
        thread.start()  
        
    def On_Run_cal(self): 
        basic_setting=self.panel_c.get_setting()
        bers=float(basic_setting["BER"]) 
        dtd=float(basic_setting["DTD"]) 
        tie=int(basic_setting["TIE"]) 
        N=round(erfcinv(bers/(0.5*dtd))*(8**0.5),3)
        Eye_pp=round(tie*N,2)
        self.panel_c.txt_N.SetValue (str(N))
        self.panel_c.txt_eye_pp.SetValue (str(Eye_pp))
        print ('\n\n\t***Simulation Done.***')
        return()        

class panel_Calculator(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)
        self.sizer=wx.GridBagSizer(hgap=10,vgap=5)    
        self.sizer.Add(wx.StaticText(self,-1,r'RMS to Eye-closure Calculator'),pos=(0,0),flag=wx.ALIGN_CENTER_VERTICAL)
        
        self.sizer.Add(wx.StaticText(self,-1,r'Specified BER (BERs)(e.g. 1e-6)'),pos=(1,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_ber=wx.TextCtrl(self,-1,"",size=(50,-1)) 
        self.sizer.Add(self.txt_ber,pos=(1,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

        self.sizer.Add(wx.StaticText(self,-1,r'Data-transition Density(DTD)'),pos=(2,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_dtd=wx.TextCtrl(self,-1,"0.5",size=(50,-1)) 
        self.sizer.Add(self.txt_dtd,pos=(2,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        
        self.sizer.Add(wx.StaticText(self,-1,'TIE random Jitter in ps RMS(e.g. \u03C3)'),pos=(3,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_tie=wx.TextCtrl(self,-1,"",size=(50,-1)) 
        self.sizer.Add(self.txt_tie,pos=(3,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        '''
        self.sizer.Add(wx.StaticText(self,-1,r'Measurement time(T)'),pos=(4,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_time=wx.TextCtrl(self,-1,"2000",size=(50,-1)) 
        self.sizer.Add(self.txt_time,pos=(4,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.sizer.Add(wx.StaticText(self,-1,r'in units of:'),pos=(4,2),flag=wx.ALIGN_CENTER_VERTICAL)
        sampleList = ['Seconds', 'Minutes', 'Hours']  
        self.u_choice = wx.ComboBox(self,-1,'Hours',(740,18),(80,20),sampleList, wx.CB_DROPDOWN)
        self.sizer.Add(self.u_choice,pos=(4,3),flag=wx.ALIGN_CENTER_VERTICAL)
        '''
        self.btn_run = wx.Button(self, 20, "Calculate", (20, 100)) 
        self.btn_run.SetToolTip("Run Analysis...")
        self.sizer.Add(self.btn_run,pos=(4,0),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL) 
        self.btn_reset = wx.Button(self, 20, "Reset", (20, 100)) 
        self.btn_reset.SetToolTip("Reset Setting...")
        self.sizer.Add(self.btn_reset,pos=(4,1),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL) 
        
        
        self.sizer.Add(wx.StaticText(self,-1,r'Crest Factor,N'),pos=(5,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_N=wx.TextCtrl(self,-1,"",size=(100,-1)) 
        self.sizer.Add(self.txt_N,pos=(5,1),span=(1,2),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.sizer.Add(wx.StaticText(self,-1,'Eye Closure in ps Peak-Peak =N\u03C3='),pos=(6,0),flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_eye_pp=wx.TextCtrl(self,-1,"",size=(100,-1)) 
        self.sizer.Add(self.txt_eye_pp,pos=(6,1),span=(1,2),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        jpg_file = wx.Image('eqn_ber_eye_closure.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.sizer.Add(wx.StaticBitmap(self, -1, jpg_file, (10 + jpg_file.GetWidth(), 5), (jpg_file.GetWidth(), jpg_file.GetHeight())),pos=(7,0),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.SetSizer(self.sizer)    
        self.sizer.Add(wx.StaticText(self,-1,r'Reference: JitterLabs website of "RMS to Eye-closure Jitter Calculator ".'),pos=(8,0),span=(1,4))
        self.sizer.Add(wx.StaticText(self,-1,r'Link:         https://www.jitterlabs.com/support/calculators/rms-eye-closure-calculator'),pos=(9,0),span=(1,4))

    def get_setting(self):
        res={}
        res["BER"]=self.txt_ber.GetValue()
        res["DTD"]=self.txt_dtd.GetValue()
        res["TIE"]=self.txt_tie.GetValue()
        return res

class panel_ref(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)        
        self.sizer=wx.GridBagSizer(hgap=10,vgap=5)  
        jpg_file = wx.Image('rms2eye_table.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.sizer.Add(wx.StaticBitmap(self, -1, jpg_file, (10 + jpg_file.GetWidth(), 5), (jpg_file.GetWidth(), jpg_file.GetHeight())),pos=(0,0),span=(1,1),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.SetSizer(self.sizer)    
        self.sizer.Fit(self)    
        self.Fit 
        
class panel_version(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,*args,**kwargs)        
        self.sizer=wx.GridBagSizer(hgap=10,vgap=5)  
        self.sizer.Add(wx.StaticText(self,-1,'version 0.1:Initial Release'),pos=(0,0))
        self.sizer.Add(wx.StaticText(self,-1,'yanbin_c@hotmail.com'),pos=(1,0))
        self.SetSizer(self.sizer)    
        self.sizer.Fit(self)    
        self.Fit 

if __name__ == "__main__":
    app = wx.App()
    frame=MyFrame()
    frame.Show()
    app.MainLoop()


