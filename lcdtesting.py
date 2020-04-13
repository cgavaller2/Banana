import lcddriver
import time
display = lcddriver.lcd()
time.sleep(3)
display.lcd_display_string("12345678", 1)
time.sleep(3)
display.lcd_display_string("12345678910111213141516", 1)
time.sleep(3)
display.lcd_display_string("123456789101112131415160", 1)
time.sleep(60)
