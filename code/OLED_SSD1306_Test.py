# OLED_SSD1306_Test.py
# SSD1306 OLED 128x64 I2C測試程式
# OmniXRI Jack, May 2021

from machine import Pin, I2C    # 導入 Pin, I2C相關函式庫
from ssd1306 import SSD1306_I2C # 導入 SSD1306 I2C介面OLED函式庫
import framebuf # 導入影格緩衝區函式庫
 
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)     # I2C#1初始化,設定SCL,SDA腳位及傳輸頻率       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # 顯示OLED I2C起始位址
print("I2C Configuration: "+str(i2c))                   # 顯示I2C組態 

#設定SSD1306 OLED 驅動IC相關參數 
WIDTH  = 128 # 顯示寬度像素
HEIGHT = 64  # 顯示高度像素
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c) # SSD1306 OLED初始化

oled.fill(0) # 清除OLED顯示區(全部填零)
oled.text("Hello World!",0,0) # 在座標(0,0)位置顯示字串

# 設定單色32x32像素樹莓派LOGO陣列
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
# 載入LOGO繪圖到緩衝區,32x32點,單色
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
oled.blit(fb, 96, 0) # 將LOGO繪至(96,0)位置
   
oled.show() # 更新OLED顯示內容
