# DIO_Test.py
# 數位輸出入信號GPIO測試程式
# OmniXRI Jack, May 2021

from machine import Pin # 從machine導入Pin參數設定類別

led1 = Pin(18, Pin.OUT) # 設定GP18為LED1(綠)輸出腳
led2 = Pin(21, Pin.OUT) # 設定GP21為LED2(紅)輸出腳
pb1  = Pin(17, Pin.IN, Pin.PULL_UP) # 設定GP17為PB1輸入腳，且自帶pull high電阻
pb2  = Pin(19, Pin.IN, Pin.PULL_UP) # 設定GP19為PB2輸入腳，且自帶pull high電阻


while True: # 若真則循環
    if(pb1.value() == 0): # 若PB1輸入為Low(按下)
        led1.value(1)     # 點亮LED1
    else:                 # 反之(未按)
        led1.value(0)     # 熄滅LED1

    if(pb2.value() == 0): # 若PB2輸入為Low(按下)
        led2.value(1)     # 點亮LED2
    else:                 # 反之(未按)
        led2.value(0)     # 熄滅LED2
        