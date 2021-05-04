# Board_Test.py
# Pi Pico擴充板測試程式
# DIO, AIO, OLED, I2C
# OmniXRI Jack, May 2021

from machine import Pin, I2C, ADC # 導入 Pin, I2C, ADC相關函式庫
from ssd1306 import SSD1306_I2C # 導入 SSD1306 I2C介面OLED函式庫
import framebuf # 導入影格緩衝區函式庫
import utime # 導入時間相關函式庫

led  = Pin(25, Pin.OUT) # 設定GP25為板上LED為輸出腳
led1 = Pin(18, Pin.OUT) # 設定GP18為LED1輸出腳
led2 = Pin(21, Pin.OUT) # 設定GP21為LED2輸出腳
pb1  = Pin(17, Pin.IN, Pin.PULL_UP) # 設定GP17為PB1輸入腳，且自帶pull high電阻
pb2  = Pin(19, Pin.IN, Pin.PULL_UP) # 設定GP19為PB2輸入腳，且自帶pull high電阻

pb1_prev = 0 # PB1先前狀態,0為未按下,1為按下
pb1_curr = 0 # PB1目前狀態,0為未按下,1為按下
pb2_prev = 0 # PB2先前狀態,0為未按下,1為按下
pb2_curr = 0 # PB2目前狀態,0為未按下,1為按下

voltage = machine.ADC(2) # 設定使用ADC2(GP28)
factor = 3.3 / (65535)   # 設定ADC轉換因子
 
WIDTH  = 128 # 設定OLED顯示寬度
HEIGHT = 64  # 設定OLED顯示高度
 
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)     # 設定使用I2C#1,SCL,SDA腳位及時脈頻率
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # 顯示I2C位址
print("I2C Configuration: "+str(i2c))                   # 顯示I2C組態 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # SSD1306 OLED初始化
 
# 設定單色32x32像素樹莓派LOGO陣列
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

time_start = utime.ticks_ms() # 啟動ms計時器

while True: # 永遠執行循環    
    oled.fill(0) # 清除OLED顯示區(全部填零)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB) # 載入LOGO繪圖到緩衝區,32x32點,單色 
    oled.blit(fb, 96, 0) # 將LOGO繪至(96,0)位置
    
    reading = voltage.read_u16() * factor # 讀取半固定電阻SVR1電壓並轉換成十進制
    oled.text("ADC: ",5,8) # 輸出提示字串到OLED,座標(5,8)
    oled.text(str(round(reading,2)),40,8) # 將電壓值規式化字串輸出到OLED,座標(40,8)
    
    pb1_curr = pb1.value() # 讀取PB1按鍵狀態並放入目前狀態變數中
    pb2_curr = pb2.value() # 讀取PB2按鍵狀態並放入目前狀態變數中
  
    if(pb1_curr == 0): # 若PB1輸入為Low(按下)
        led1.value(1)     # 點亮LED1
        oled.text("PB1:On",5,16) # 輸出PB1按下字串到OLED,座標(5,16)     
    else:                 # 反之未按下
        led1.value(0)     # 熄滅LED1
        oled.text("PB1:Off",5,16) # 輸出PB1未按字串到OLED,座標(5,16) 

    if(pb2_curr == 0): # 若PB2輸入為Low(按下)
        led2.value(1)     # 點亮LED2
        oled.text("PB2:On",5,24) # 輸出PB2按下字串到OLED,座標(5,24) 
    else:                 # 反之未按下
        led2.value(0)     # 熄滅LED2
        oled.text("PB2:Off",5,24) # 輸出PB2未按字串到OLED,座標(5,16)
        
    if(pb1_curr == 0 and pb1_prev == 1): # 若PB1正緣觸發
        print("PB1 Press")               # 透過USB Virual COM回傳PB1按下訊息
    
    if(pb1_curr == 1 and pb1_prev == 0): # 若PB1負緣觸發
        print("PB1 Release")             # 透過USB Virual COM回傳PB1放開訊息

    if(pb2_curr == 0 and pb2_prev == 1): # 若PB2正緣觸發
        print("PB2 Press")               # 透過USB Virual COM回傳PB1按下訊息
        
    if(pb2_curr == 1 and pb2_prev == 0): # 若PB2負緣觸發
        print("PB2 Release")             # 透過USB Virual COM回傳PB1放開訊息
        
    pb1_prev = pb1_curr # 將PB1目前狀態更新到先前狀態
    pb2_prev = pb2_curr # 將PB2目前狀態更新到先前狀態

    oled.show() # 更新OLED顯示區內容
    
    time_stop = utime.ticks_ms() # 取得目前時間
    
    if utime.ticks_diff(time_stop,time_start) > 500: # 若先前時間比較大於0.5秒
        led.toggle()          # 則板上LED狀態反轉
        time_start = time_stop # 更新目前時間到先前時間
