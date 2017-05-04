# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 09:48:48 2017

@author: ZQ
"""
import numpy as np
import pandas as pd
from WindPy import w
import datetime as dt
import sys
import os

w.start()


# function for updating the 'base' file
def UpdateBase(today, more_fields = str(), path = 'D:\\qi'):    # 'fields' contains basic fields already, if more fields wanted, 
        # put them in 'more_fields' with str type 'xxx, yyyy, zzzz', 'path' is where you want to save your data file
    os.chdir(path)
    fields = 'sec_name,isin_code,comp_name,comp_name_eng,ipo_date,delist_date'    
    
    if len(more_fields)>0:
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
    baseinfo.to_csv(path + '\\base.csv', index = False)


# function for updating the data file
def UpdateData(today, more_fields = str(), path = 'D:\\qi'):
     # 'basicfields' contains basic fields ('open,close,high,low,volume,amt,turn,trade_status') already, if more fields wanted, 
        # put them in 'more_fields' with str type 'xxx, yyyy, zzzz'
        # Also change 'path' for the path to save all the data as you want
    os.chdir(path)
    tradingdays = pd.read_csv('tradingdays.csv')    # 'tradingdays.csv' contains all the days which HAVE BEEN UPDATED, there
                                                                   # there is a example file in the fold
    lastday = tradingdays.iloc[len(tradingdays)-1]['days']
    days = w.tdays(lastday, str(today)).Times
    days = [str(x.date()) for x in days]                           # 'days' are the days need to be update
    dayid = [(dt.datetime.strptime(x,'%Y-%m-%d').date() - dt.date(1900,1,1)).days for x in days]
    daymap = pd.DataFrame({'dayid':dayid, 'days':days})
    p = len(days)
    
    basicfields = 'open,close,high,low,volume,amt,turn,trade_status'
    otherfields = 'total_shares,free_float_shares,ev,eps_basic,eps_exbasic,pb_lf,roe_avg,roe_deducted,debttoassets,netprofitmargin,grossprofitmargin'
    otherfields = otherfields + more_fields
    basicfields_split = basicfields.split(',')      # get column names
    otherfields_split = otherfields.split(',')
    
    if p>1:
        for i in range(p-1):
            cursor_today = days[i+1]
            m = 0
            while m < 3:
                todaymarketdata = np.transpose(pd.DataFrame(w.wset('SectorConstituent', 'date=' + str(cursor_today) + ';sector=全部AB股').Data))
                m = len(todaymarketdata.columns)
            code = todaymarketdata[1].values.tolist()
            code = code[:6]      # use this line and uncommend the former one line to test codes with less time and memory required
            m = len(code)
            tradeday = 'tradeDate=' + str(cursor_today)
            
            ClosePrice = np.transpose(pd.DataFrame(w.wss(code, 'close', tradeday, 'PriceAdj=B').Data))
            BasicStockData = np.transpose(pd.DataFrame(w.wss(code, basicfields, tradeday, 'priceAdj=U', 'cycle=D').Data))
            OtherStockData = np.transpose(pd.DataFrame(w.wss(code, otherfields, tradeday).Data))
            BasicStockData.columns = basicfields_split
            OtherStockData.columns = otherfields_split

            
            CSRCCode = np.transpose(pd.DataFrame(w.wss(code, 'industry_CSRCcode12', tradeday, 'industryType=3').Data))
            SWCode = np.transpose(pd.DataFrame(w.wss(code,'industry_swcode', tradeday, 'industryType=1').Data))
            GICSCode = np.transpose(pd.DataFrame(w.wss(code, 'industry_gicscode', tradeday, 'industryType=4').Data))
            SH50 = np.transpose(pd.DataFrame(w.wss(code, 'compindex2', tradeday, 'index=1').Data))
            SH180 = np.transpose(pd.DataFrame(w.wss(code, 'compindex2', tradeday, 'index=2').Data))    
            HS300 = np.transpose(pd.DataFrame(w.wss(code, 'compindex2', tradeday, 'index=3').Data))        
            HH100 = np.transpose(pd.DataFrame(w.wss(code, 'compindex2', tradeday, 'index=4').Data))
            SZ100 = np.transpose(pd.DataFrame(w.wss(code, 'compindex2', tradeday, 'index=5').Data))
            # CategoryName = np.transpose(pd.DataFrame(w.wss(code, 'industry_CSRC12,industry_sw,industry_gics', tradeday 'industryType=1').Data))

            errorsum = [np.sum(x.shape) for x in [ClosePrice, BasicStockData, OtherStockData, CSRCCode, SWCode, GICSCode, SH50, SH180, \
                        SH180, HS300, HH100, SZ100]]
            
            if 2&0 in errorsum:
                sys.exit('Can not download data from Wind now on ' + str(cursor_today))   # exit the program when data downloading is unsuccessful

            HH500 = HH100
            HH500[:] = 0
            
            CirculationMarketValue = OtherStockData['ev'] * OtherStockData['free_float_shares'] / OtherStockData['total_shares'] 
            SRCCode = [(ord(x[:1]) - 65) * 1000 +int(x[1:3]) for x in (CSRCCode[0].values.tolist())]
            SRCCode = pd.DataFrame(SRCCode)
            SWCode[0] = SWCode[0].str[0:6]            
            BasicStockData['trade_status'][BasicStockData['trade_status'] != '交易'] = 0   # here, 交易 means listing 
            BasicStockData['trade_status'][BasicStockData['trade_status'] == '交易'] = 1
            SH50[0][SH50[0] == '是'] =1                                  # here, 是 means this stock belongs to this stock index, while 否 means not
            SH50[0][SH50[0] == '否'] =0
            SH180[0][SH180[0] == '是'] =1
            SH180[0][SH180[0] == '否'] =0
            HS300[0][HS300[0] == '是'] =1
            HS300[0][HS300[0] == '否'] =0
            HH100[0][HH100[0] == '是'] =1
            HH100[0][HH100[0] == '否'] =0     
            SZ100[0][SZ100[0] == '是'] =1
            SZ100[0][SZ100[0] == '否'] =0     
            
            Date = ClosePrice.copy()
            Date[:] = cursor_today
            alldata = [Date, ClosePrice, BasicStockData, CirculationMarketValue, OtherStockData, SRCCode, SWCode,\
                  GICSCode, SH50, SH180, HS300, HH100, SZ100, HH500]
            csvdata = pd.concat(alldata, 1)
            
            allcolnames =  ["Date", "ClosePrice","OriOpenPrice","OriClosePrice","OriHighPrice","OriLowPrice",\
                  "TradeVolume","TradeAmount","Turnover","Tradable",\
                  "CirculationMarketValue","TotalStock","CirculationStock","TotalMarketValue",\
                  "EPS","EPS_EX","PBRatio","ROE_AVG","ROE_EX","Leverage","NetProfitMargin","GrossMargin",\
                  "SRCCode","SWCode","WDCode","SH50Flag","SH180Flag","HS300Flag","HH100Flag","SZ100Flag","HH500Flag"]
            if len(more_fields)>0:
                  allcolnames = allcolnames.extend(more_fields.split(','))
            # 'allcolnames' contains all the fields name we got
            csvdata.columns = allcolnames
            rownum = csvdata.shape[0]
            
            
            if not os.path.exists(path + '\\data'):       # make the dir 'data' to save all the stock data
                os.makedirs(path + '\\data')
                
                
            for j in range(rownum):
                if os.path.exists(path + '\\data\\{}.csv'.format(code[j])):
                    data = pd.read_csv(path + '\\data\\{}.csv'.format(code[j]), header = 0)
                    q = len(data)
                    if True in csvdata.iloc[j].isnull().values:
                        napos = csvdata.columns[csvdata.iloc[j].isnull()]
                        if True in data.iloc[(q-1)][napos].isnull().values:
                            napos = napos.drop(data.columns[data.iloc[(q-1)].isnull()].tolist())
                        csvdata.iloc[j][napos] = data.iloc[(q-1)][napos].copy()
                    data = data.append(csvdata.iloc[j])
                    data.to_csv(path + '\\data\\{}.csv'.format(code[j]), index = False, header = True)
                else:
                    (pd.DataFrame(csvdata.iloc[j]).T).to_csv(path + '\\data\\{}.csv'.format(code[j]), index = False, header =True)
            tradingdays = tradingdays.append(daymap.iloc[i+1])                                 # record the new dates we have updated
            tradingdays.to_csv('tradingdays.csv', index = False, header = True)
            