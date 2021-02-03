# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 21:40:23 2020

@author: USER
"""

import ccxt
#import csv
import datetime
import time
import requests
import sys
import json
import traceback

exchange_list = ['aofex', 'bequant', 'bitkk', 'bitmax', 'gateio', 'hitbtc', 
                 'hollaex', 'huobipro','kucoin', 'latoken', 'lbank', 'okex']

gap_retrieval_interval=5
gap_recheck_interval=10
gap_fetch_interval=25

aofex=ccxt.aofex();bequant=ccxt.bequant();bitkk=ccxt.bitkk();bitmax=ccxt.bitmax();
gateio=ccxt.gateio();hitbtc=ccxt.hitbtc();hollaex=ccxt.hollaex();huobipro=ccxt.huobipro();
kucoin=ccxt.kucoin();latoken=ccxt.latoken();lbank=ccxt.lbank();okex=ccxt.okex();

lbank.apiKey='26b170f8-d842-49f2-a97d-d2c9d8fbf69e'
lbank.secret='MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKGUSuql25yd1YQHrwSm9JUglV+ExhaTHVEFx08ekYmxZ1fI0Ly888fEQKlVmuMBlCYWMejA8JKvSL5tndawzPL/2nEjf99TuTeTXJoxnbyKeO5v62vKCg1ZKr39VPsKFJWeJj6r2xv4YhjCRSpfQex4cW8Ptb0evPMluom7bAf5AgMBAAECgYArhJgk2KTsaqoeFD+0Hg9TtuHkRwte+yJzNv42NgJ2tlwiDYkCvFVgIWBU+yRrLXqsQ2AP0x84MpOCDl3re9TG0chAW5vQMZSMd/ecg/KQARQUsMWS9YE97BUeqEgkUUHhW9fx6qxswYWCNzg4FPz77Pi8SOnAiHV88wPKtIUhnQJBAPvKwp+JdzRvx2DqISdDTnKFWj73qWLFkP6jlLZwkGZCks6LW5WDSI2BlbbMFW9+lQ8pJBC50xOlTRl9w79/LGcCQQCkR5Ns07tdvguM3/d5JM/DzSXsff7WiO+MtY+84WuP9lj+jFf2IEHKEttrC1R5HAuwg34CepSomWtcEWmFLGyfAkBuv75fIb226LuPmyu981Lb+F+7dn+gnDmsZxMQM+6vq/SauJ0t5DLTWv4ZCycahVjW9EeSu8llyL1iyviAkFVdAkACYufJVOoL2o7gZQB7SgWamohKfyoMg8C3Eowb+kpNtQ5l5DQC50UNYmi9jVSUzct9rOtPregq6s+cbsRRouuRAkAtlNZ4Ag7uj9n67ClneAQKguDvUeZLBbQF0s2hFIaeYwEqcuo8mLECjWc35xSS8DZwnRzg8pu8Uo/8S10UWhEU'
line_token='QcmhPgDAY69Sit9fxbJzy8lE5C98bumPzSHcSbe3UyX'


def short_entry(xrp_balance, usdt_balance):
    
    lbank_ticker=lbank.fetch_ticker('XRP/USDT')
    lbank_last=lbank_ticker['last']
    adjusted_rate_for_limit_sell=lbank_last*0.01
    
    lbank.create_order(
            symbol='XRP/USDT',
            type='limit',
            side='sell',
            amount=xrp_balance,
            price=adjusted_rate_for_limit_sell)
    
    time.sleep(10)

    
def short_cover(xrp_balance, usdt_balance):
    
    side='short'

    lbank_ticker=lbank.fetch_ticker('XRP/USDT')
    lbank_last=lbank_ticker['last']
    
    adjusted_rate_for_limit_buy=lbank_last*1.05
    
    lbank.create_order(
            symbol='XRP/USDT',
            type='limit',
            side='buy',
            amount=xrp_balance,
            price=adjusted_rate_for_limit_buy)
    
    time.sleep(10)
    
    balance_after_transaction=lbank.fetch_balance()
    usdt_transaction_result=balance_after_transaction['total']['USDT']
    xrp_transaction_result=balance_after_transaction['total']['XRP']
                    
    usdt_gain=str(((usdt_transaction_result-usdt_balance)/usdt_balance)*100)+'%'
    xrp_gain=str(((xrp_transaction_result-xrp_balance)/xrp_balance)*100)+'%'
    
    transaction_info={'side':side, 'usdt_transaction_result': usdt_transaction_result,
                      'usdt_gain':usdt_gain, 'xrp_transaction_result':xrp_transaction_result,
                      'xrp_gain':xrp_gain}
    
    return transaction_info


def long_entry(xrp_balance, usdt_balance):
    
    lbank_ticker=lbank.fetch_ticker('XRP/USDT')
    lbank_last=lbank_ticker['last']
    #adjusted_rate_for_limit_buy=lbank_last*1.05
    #ordered_xrp_amount=xrp_balance*0.5
    adjusted_rate_for_limit_buy=lbank_last*1.05
    ordered_xrp_amount=usdt_balance*0.95/lbank_last
    
    lbank.create_order(
            symbol='XRP/USDT',
            type='limit',
            side='buy',
            amount=ordered_xrp_amount,
            price=adjusted_rate_for_limit_buy)
    
    return ordered_xrp_amount

    
def long_cover(xrp_balance, usdt_balance, ordered_xrp_amount):

    side='long'
    
    lbank_ticker=lbank.fetch_ticker('XRP/USDT')
    lbank_last=lbank_ticker['last']
    adjusted_rate_for_limit_sell=lbank_last*0.01
    
    lbank.create_order(
            symbol='XRP/USDT',
            type='limit',
            side='sell',
            amount=ordered_xrp_amount,
            price=adjusted_rate_for_limit_sell)
    
    time.sleep(10)
    
    balance_after_transaction=lbank.fetch_balance()
    usdt_transaction_result=balance_after_transaction['total']['USDT']
    xrp_transaction_result=balance_after_transaction['total']['XRP']
                    
    usdt_gain=str(((usdt_transaction_result-usdt_balance)/usdt_balance)*100)+'%'
    xrp_gain=str(((xrp_transaction_result-xrp_balance)/xrp_balance)*100)+'%'
    
    transaction_info={'side':side, 'usdt_transaction_result': usdt_transaction_result,
                      'usdt_gain':usdt_gain, 'xrp_transaction_result':xrp_transaction_result,
                      'xrp_gain':xrp_gain}
    
    return transaction_info

def fetch_lbank_gap(exchange_list):
    
    count=1
    supporting_count=0
    
    last_prices=[]

    for exchange in exchange_list:
         
         try:
             xrpusdt_ticker = eval(exchange+ ".fetch_ticker ('XRP/USDT')")
             last=xrpusdt_ticker['last']
             last_prices.append(last)
             supporting_count+=1
             
             if supporting_count<2:
                 pass
             else:
                 count+=1
                 
         except:
             last=0
             last_prices.append(last)
             
             if supporting_count==0:
                 count-=1
             
             else:
                 pass
    
    last_ave=sum(last_prices)/count
    
    lbank_ticker=lbank.fetch_ticker('XRP/USDT')
    lbank_last=lbank_ticker['last']
    
    lbank_gap=(lbank_last-last_ave)/last_ave
    
    return lbank_gap, count


def note(transaction):
    
    dt_now_datetime=datetime.datetime.now()
    dt_now=dt_now_datetime.strftime('%Y-%m-%d %H:%M:%S')
    transaction['dt_now']=dt_now

    with open('C:\Ripplage\価格変遷スタディー\Ripplage稼働_2.csv', 'a', newline='') as f:
          
        print (transaction, file=f)
        
        """
        writer = csv.writer(f)
        writer.writerow(transaction)
        """    
        
    return transaction

def line_notify( text ):
	url = "https://notify-api.line.me/api/notify"
	data = {"message" : text}
	headers = {"Authorization": "Bearer " + line_token} 
	requests.post(url, data=data, headers=headers)



try:
    
    while True:
    
        lbank_balance=lbank.fetch_balance()
        xrp_balance=lbank_balance['total']['XRP']
        usdt_balance=lbank_balance['total']['USDT']
    
        lbank_gap_tuple=fetch_lbank_gap(exchange_list)
        lbank_gap=lbank_gap_tuple[0]
        count=lbank_gap_tuple[1]

        if abs(lbank_gap)<0.0001:
                lbank_gap=0
    
        else:
            pass
        
        print (lbank_gap)
    
        if abs(lbank_gap)>0.0165 and abs(lbank_gap)<0.05 and count==12:
        
            lbank_ticker=lbank.fetch_ticker('XRP/USDT')
            gapped_lbank_last=lbank_ticker['last']  
        
            if lbank_gap>0:
                
                line_notify('shortでentryします'+str(lbank_gap))
            
                short_entry(xrp_balance, usdt_balance)        
                time.sleep(gap_retrieval_interval)
            
                lbank_gap_for_cover_tuple=fetch_lbank_gap(exchange_list)
                lbank_gap_for_cover=lbank_gap_for_cover_tuple[0]
            
            
                while lbank_gap_for_cover>0:
                
                    time.sleep(gap_recheck_interval)
                    lbank_gap_for_cover_tuple=fetch_lbank_gap(exchange_list)
                    lbank_gap_for_cover=lbank_gap_for_cover_tuple[0]


                lbank_ticker_for_cover=lbank.fetch_ticker('XRP/USDT')
                retrieved_lbank_last=lbank_ticker_for_cover['last']
            
                transaction=short_cover(xrp_balance, usdt_balance)
            
            
                transaction['lbank_gap']=lbank_gap
                transaction['lbank_gap_for_cover']=lbank_gap_for_cover
                transaction['gapped_lbank_last']=gapped_lbank_last
                transaction['retrieved_lbank_last']=retrieved_lbank_last
            
                execution_data=note(transaction)
                string_execution=json.dumps(execution_data)
            
                print(string_execution)
                line_notify(string_execution)
        
            else:
                
                line_notify('longでentryします'+str(lbank_gap))
            
                ordered_xrp_amount=long_entry(xrp_balance, usdt_balance)
            
                time.sleep(gap_retrieval_interval)
            
                lbank_gap_for_cover_tuple=fetch_lbank_gap(exchange_list)
                lbank_gap_for_cover=lbank_gap_for_cover_tuple[0]

            
                while lbank_gap_for_cover<0:
                    time.sleep(gap_recheck_interval)
                    lbank_gap_for_cover_tuple=fetch_lbank_gap(exchange_list)
                    lbank_gap_for_cover=lbank_gap_for_cover_tuple[0]

            
                lbank_ticker_for_cover=lbank.fetch_ticker('XRP/USDT')
                retrieved_lbank_last=lbank_ticker_for_cover['last']

                transaction=long_cover(xrp_balance, usdt_balance, ordered_xrp_amount)
            
            
                transaction['lbank_gap']=lbank_gap
                transaction['lbank_gap_for_cover']=lbank_gap_for_cover
                transaction['gapped_lbank_last']=gapped_lbank_last
                transaction['retrieved_lbank_last']=retrieved_lbank_last
            
                execution_data=note(transaction)
                string_execution=json.dumps(execution_data)
            
                print(string_execution)
                line_notify(string_execution)
            
        else:
             time.sleep(gap_fetch_interval)


except:
    print ('エラーが発生しました')
    line_notify('エラーが発生しました。稼働を中止します。')
    traceback.print_exc()
    sys.exit()

        