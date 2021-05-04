# Remote_Test.py
# 從USB虛擬COM遠端異步發送命令及接收資料測試程式
# OmniXRI Jack, May 2021

from machine import Pin, I2C, ADC # 導入 Pin, I2C, ADC相關函式庫
from ssd1306 import SSD1306_I2C # 導入 SSD1306 I2C介面OLED函式庫
import framebuf # 導入影格緩衝區函式庫
import utime # 導入時間相關函式庫
import sys # 導入系統標準輸出入相關函式庫
import select # 導入異步選擇函式庫

led  = Pin(25, Pin.OUT) # 設定GP25為板上LED為輸出腳
led1 = Pin(18, Pin.OUT) # 設定GP18為LED1輸出腳
led2 = Pin(21, Pin.OUT) # 設定GP21為LED2輸出腳

voltage = machine.ADC(2) # 設定使用ADC2(GP28)
factor = 3.3 / (65535)   # 設定ADC轉換因子
 
WIDTH  = 128 # 設定OLED顯示寬度
HEIGHT = 64  # 設定OLED顯示高度
 
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)     # 設定使用I2C#1,SCL,SDA腳位及時脈頻率
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # 顯示I2C位址
print("I2C Configuration: "+str(i2c))                   # 顯示I2C組態 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # SSD1306 OLED初始化

time_start = utime.ticks_ms() # 啟動ms計時器
 
while True: # 永遠執行循環    
    oled.fill(0) # 清除OLED顯示區(全部填零)
    
    # 若有收到遠端透過USB虛擬COM傳送命令字串時才進行命令
    # 採異步(不阻塞)命令執行方式完成
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        
        s = sys.stdin.readline().strip() #從標準輸人讀取一行文字並去除換行符號
        cmd = str(s) # 將收到的內容轉成字串
        print(cmd) # 回傳檢查收到之命令內容,可省略
        
        if cmd == 'G0':   # 若命令為G0      
            led1.value(0) # 熄滅LED1
        elif cmd == 'G1': # 若命令為G1   
            led1.value(1) # 點亮LED1
        elif cmd == 'R0': # 若命令為R0        
            led2.value(0) # 熄滅LED2
        elif cmd == 'R1': # 若命令為R1   
            led2.value(1) # 點亮LED2
        else:             # 其它命令
            oled.text(cmd,0,32) # 顯示收到命令內容

    reading = voltage.read_u16() * factor # 讀取半固定電阻SVR1電壓並轉換成十進制
    oled.text("ADC: ",5,8) # 輸出提示字串到OLED,座標(5,8)
    oled.text(str(round(reading,2)),40,8) # 將電壓值規式化字串輸出到OLED,座標(40,8)
    oled.show() # 更新OLED顯示區內容
    
    time_stop = utime.ticks_ms() # 取得目前時間
    
    if utime.ticks_diff(time_stop,time_start) > 500: # 若先前時間比較大於0.5秒
        led.toggle()          # 則板上LED狀態反轉
        time_start = time_stop # 更新目前時間到先前時間
