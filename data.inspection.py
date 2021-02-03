# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 00:46:43 2020

@author: USER
"""

import json
import numpy as np
import matplotlib.pyplot as plt

f = open("C:\Ripplage\価格データ.json", "r")
data = json.load(f)

#移動平均線と標準偏差の期間
term=20


def std_in_term (term, i, data):
    
    close_prices=[]
    count=1
    
    while count<=term:
        close_prices.append(data[i-(term)+count]['close_price'])
        count+=1
    
    ave=sum(close_prices)/len(close_prices)
    std=np.std(close_prices)
    
    return ave, std

#終値のリストを作る
close_prices=[]

count1=19

for datum in data:
    close_price=data[count1]['close_price']
    close_prices.append(close_price)
    count1+=1

#20期間移動平均線のリストを作る
ave_list=[]




#20期間標準偏差のリストを作る

#1シグマのリストを作る

#2シグマのリストを作る
    
#-1シグマのリストを作る
    
#-2シグマのリストを作る
    
#0~5999の整数のリストを作る
    




x1 = [100, 200, 300, 400, 500, 600]
y1 = [10, 20, 30, 50, 80, 130]

x2 = x1
y2 = x1

plt.plot(x1, y1, color = 'red', marker = 'o')

plt.plot(x2, y2, color = 'blue', marker = 'v')
plt.show()

