# -*- coding: utf-8 -*-
"""
Created on Thu May 4 21:31:20 2017

@author: Zhao, Qi
"""
import datetime as dt

from UpdateFuns import UpdateBase as UB
from UpdateFuns import UpdateData as UD

today = str(dt.date.today())

path =    # Set the path you wanted here before running, and BESURE to save my example file 'tradingdays.csv' to this path before running 

UB(today, more_fields = str(), path)
UD(today, more_fields = str(), path)
