# coding: utf-8

# Integrated by Qi, on 05-02-2017.
# The functions below are for creating several files which contain important data while doing quantitative research in stock market or 
# constructing algorithm trading strategies. 


import numpy as np
import pandas as pd
from WindPy import w
import datetime as dt
import sys
import os


w.start()

#----------------------------------
# Part I: Creating the function for updating the 'base' file
# Here, the 'base' file includes the fields like name, code, company's name, ipo date and so on basic information of all the stocks 
# (listing and delisted stocks)
#----------------------------------

def UpdateBase(today, more_fields = None, path = str()):    # 'fields' contains basic fields already, if more fields wanted, 
        # put them in 'more_fields' with str type 'xxx, yyyy, zzzz', if not current path required, add complete str path in ‘path'
    fields = 'sec_name,isin_code,comp_name,comp_name_eng,ipo_date,delist_date'    
    
    if more_fields != None:
        fields = fields + ',' + more_fields   # includes more fields wanted
    
    fields_split = fields.split(',')      # get column names
    todaymarketdata = np.transpose(pd.DataFrame(w.wset('SectorConstituent', 'date=' + str(today) + ';sector=全部AB股').Data))
    todaymarketdata = todaymarketdata.set_index([0])
    code = todaymarketdata[1].values.tolist()
    baseinfo1 = np.transpose(pd.DataFrame(w.wss(code, fields, 'tradeDate=' + str(today)).Data))
    baseinfo1 = baseinfo1.rename(columns=lambda x: fields_split[x])   # name the column of dataframe
    baseinfo1['ipo_date'] = [str(x.date()) for x in baseinfo1['ipo_date']]   # change the type to str
    baseinfo1['delist_date'] = [str(x.date()) for x in baseinfo1['delist_date']]
    
    todaymarketdata = np.transpose(pd.DataFrame(w.wset('SectorConstituent', 'date=' + str(today) + ';sector=已摘牌股票').Data))
    todaymarketdata = todaymarketdata.set_index([0])
    code = todaymarketdata[1].values.tolist()
    baseinfo2 = np.transpose(pd.DataFrame(w.wss(code, fields, 'tradeDate=' + str(today)).Data))
    baseinfo2 = baseinfo2.rename(columns=lambda x: fields_split[x])
    baseinfo2['ipo_date'] = [str(x.date()) for x in baseinfo2['ipo_date']]
    baseinfo2['delist_date'] = [str(x.date()) for x in baseinfo2['delist_date']]
    baseinfo = pd.concat([baseinfo1, baseinfo2])
    baseinfo.to_csv(path + 'base.csv', index = False)
