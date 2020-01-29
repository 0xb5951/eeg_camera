## This Source is M5StickV MaixPy
import network, socket, time, sensor, image,lcd
from Maix import GPIO
from fpioa_manager import fm, board_info
from machine import UART

'''
function define
'''
def camera_setup():
    lcd.direction(lcd.YX_LRUD)
    sensor.reset()
    sensor.set_framesize(sensor.QQVGA)
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.run(1)
    sensor.skip_frames(time = 2000)

'''
main function
'''
lcd.init()
camera_setup()

#M5StickV GPIO_UART
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO5, force=True)

#M5StickV main button
main_button = GPIO(GPIO.GPIO5, GPIO.IN, GPIO.PULL_UP)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
receive_data = ''
while True:
    img = sensor.snapshot()
    if receive_data == b'kacha':
        lcd.display(img)
        img_buf = img.compress(quality=70)
        # スタートビット
        img_size1 = (img.size()& 0xFF0000)>>16
        img_size2 = (img.size()& 0x00FF00)>>8
        img_size3 = (img.size()& 0x0000FF)>>0
        data_packet = bytearray([0xFF,0xD8,0xEA,0x01,img_size1,img_size2,img_size3,0x00,0x00,0x00])
        uart_Port.write(data_packet)
        # 画像データ送信
        uart_Port.write(img_buf)
        print('send uart')
        time.sleep(1)
    #receive data from stickc
    receive_data = uart_Port.read()
    print(receive_data)
    time.sleep(1)

