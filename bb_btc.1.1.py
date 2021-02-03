# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 08:37:49 2020

@author: USER
"""

import json
import numpy as np

f = open("C:\Ripplage\価格データ.json", "r")
data = json.load(f)
#dataは1時間足のロー測データ5999個分

#移動平均、BBの計算期間
term=20

#スクイーズを定義する期間
squeeze_term=15

#ARを取得する期間
average_range_term=5

#最小標準偏差がでてから何期間までsqueezeが持続しているとみなすか
squeeze_flag=4

#ARの何倍の実線の長さでsigma2をブレイクした際1期間で直ちにトレンド発生とみなすか
quick_trend_change_rate=2.5

#一つの期間に対して標準偏差を作る関数。term, i, data[リスト]を入れ、標準偏差と移動平均を返す。
def std_in_term (term, i, data):
    
    close_prices=[]
    count=1
    
    while count<=term:
        close_prices.append(data[i-(term)+count]['close_price'])
        count+=1
    
    ave=sum(close_prices)/len(close_prices)
    std=np.std(close_prices)
    
    return ave, std

#特定の期間average_range_termでのARを返す
def get_average_range (average_range_term, i, data):
    
    range=[]
    count=1
    
    while count<=term:
        single_range=abs(data[i-average_range_term+count]['open_price']-data[i-average_range_term+count]['close_price'])
        range.append(single_range)
        count+=1
    
    average_range=sum(range)/len(range)
    
    return average_range

#スクイーズがおきているかどうか判定する関数
def check_squeeze(std_list, squeeze_term, squeeze_flag):
    
    std_list_for_squeeze=[]
    count=0
    
    while count<squeeze_term:
        std=std_list[-(squeeze_term-count)]
        std_list_for_squeeze.append(std)
        count+=1
    
    minimum_std=min(std_list_for_squeeze)
    
    std_list_in_squeeze_flag=[]
    count2=1
    
    while count2<=squeeze_flag:
        std_list_in_squeeze_flag.append(std_list_for_squeeze[-count2])
        count2+=1
        
    if minimum_std in std_list_in_squeeze_flag:
        return True
    else:
        return False
    

#所与の終値がARのquick_trend_change_rate倍の長さで2シグマをブレイクしているか

def check_quick_trend_change(average_range, std, ave, quick_trend_change_rate, data, i):

    #まず、所与のローソクの長さをcandle_lengthに入れる
    candle_length=data[i]['close_price']-data[i]['open_price']
    
    if candle_length>quick_trend_change_rate*average_range:
        pass
    
    else:
        return False
    
    if candle_length>=0:
        
        if data[i]['close_price']>ave+2*std:
            return True
        else:
            return False
    else:
        
        if data[i]['close_price']<ave-2*std:
            return True
        
        else:
            return False

def serial_candle (i, data, std_list, ave_list):
    
    current_open_price=data[i]['open_price']
    previous_open_price=data[i]['open_price']
    
    current_close_price=data[i]['close_price']
    previous_close_price=data[i]['close_price']
    
    two_close_price_relation=current_close_price-previous_close_price
    two_open_price_relation=current_open_price-previous_open_price
    
    if current_close_price>ave_list[-1]:
        
        #シグマ2を二本連続でブレイクし、始値と終値が両方切りあがっているか
        previous_sigma2=ave_list[-2]+2*std_list[-2]
        current_sigma2=ave_list[-1]+2*std_list[-1]
        
        if previous_close_price>previous_sigma2 \
        and current_close_price>current_sigma2 \
        and two_close_price_relation>0 \
        and two_open_price_relation>0:
            
            return True
        else:
            return False
    
    else:
        previous_sigma2=ave_list[-2]-2*std_list[-2]
        current_sigma2=ave_list[-1]-2*std_list[-1]
        
        if previous_close_price<previous_sigma2 \
        and current_close_price<current_sigma2 \
        and two_close_price_relation<0 \
        and two_open_price_relation<0:
            
            return True
        
        else:
            return False

def check_expansion (std_list, average_range, average_range_term):
    
    recent_sigmas=[]
    
    count=-(average_range_term)
    
    while count<0:
        recent_sigmas.append(std_list[count])
        count+=1
    
    max_recent_sigma=max(recent_sigmas)
    
    if 2*max_recent_sigma> 3*average_range:
        
        return True
    
    else:
        return False
    
def check_serial_candle(data, i, position):
    
    current_candle=data[i]['close_price']-data[i]['open_price']
    previous_candle=data[i-1]['close_price']-data[i-1]['open_price']
    
    if position=='sell':
        
        if current_candle>0 and previous_candle>0:
            return True
        else:
            pass
    else:
        
        if current_candle<0 and previous_candle<0:
            return True
        else:
            pass
        
def check_contrary_candle (data, i, position):
    current_candle=data[i]['close_price']-data[i]['open_price']
        
    if position=='sell' and current_candle>0:
        return True
    elif position=='buy' and current_candle<0:
        return True
    else:
        return False
    
def check_big_contrary (average_range, data, i, position):
    latest_candle_range=data[i]['close_price']-data[i]['close_price']
        
    if position=='long':
            
        if latest_candle_range<0 and abs(latest_candle_range)>average_range:
                
            return True
        else:
            pass
    else:
        if latest_candle_range>0 and abs(latest_candle_range)>average_range:
            
            return True
        else:
            pass


position='OFF'    
i=term
contrary_candle=0

while i<5999:
    
    if position=='OFF':
        
        #stdリストを作る。
        std_list=[]
    
        #aveリストを作る。
        ave_list=[]
    
        count1=1
    
        while count1<=term:
        
            ave, std=std_in_term(term, i-term+count1, data)
            std_list.append(std)
            ave_list.append(ave)
            count1+=1
    
        #term中のclose_priceのリストを作る
        close_price_list=[]
        count2=1
    
        while count2<=term:
        
            close_price=data[i-term+count2]['close_price']
            close_price_list.append(close_price)
            count2+=1
    
        average_range=get_average_range(average_range_term, i, data)
        squeeze=check_squeeze(std_list, squeeze_term, squeeze_flag)
        expansion=check_expansion (std_list, average_range, average_range_term)
        
        if squeeze and not expansion:
            
            quick_trend_change=check_quick_trend_change(average_range,
                                                        std,
                                                        ave,
                                                        quick_trend_change_rate,
                                                        data,
                                                        i)

            serial_candles=serial_candle (i, data, std_list, ave_list)
            
            if quick_trend_change or serial_candles:
                #エントリーのコード
                print(str(i)+'回目でエントリーです')
                
                position='sell'#か'buy'
                
            else:
                pass
        else:
            pass

    else:
        pass
        """
     
        if check_contrary_candle (data, i, position):
            contrary_candle+=1
        else:
            pass
        
        average_range=get_average_range(average_range_term, i, data)
    
        if contrary_candle>2\
        or check_serial_candle(data, i, position)\
        or check_big_contrary(average_range, data, i, position):
            
            #手じまいのコードを実装
            print(str(i)+'回目でカバーです')
            position=='OFF'
        else:
            pass
            
        """
        
            
    i+=1
