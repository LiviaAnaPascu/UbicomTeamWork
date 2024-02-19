#   •  -1,1- • -1,2- •
#   |        |       |
#  2,1   1  2,2   2  2,3
#   |        |       |
#   •  -3,1- • -3,2- •
#   |        |       |
#  4,1  3   4,2  4  4,3
#   |        |       |
#   •  -5,1- • -5,2- •

# Box 1: [(1, 1), (2, 2), (3, 1), (2, 1)]
# Box 2: [(1, 2), (2, 3), (3, 2), (2, 2)]
# Box 3: [(3, 1), (4, 2), (5, 1), (4, 1)]
# Box 4: [(3, 2), (4, 3), (5, 2), (4, 2)]
from machine import Pin
from time import sleep
import ujson
import usocket as socket
import network
import urequests


Off, On, isPressed, NotPressed = False, True, True, False

#BUTTONS SETUP
buttons_total_rows = 3
buttons_total_columns = 4

button_column_pins = [Pin(36, Pin.IN), Pin(37, Pin.IN), Pin(38, Pin.IN),Pin(39, Pin.IN)]
button_mux_a, button_mux_b = Pin(34, Pin.IN), Pin(35, Pin.IN)

buttons = [[NotPressed for _ in range(buttons_total_columns)] for _ in range(buttons_total_rows)]

def getRow(): 
    muxA = button_mux_a.value()
    muxB = button_mux_b.value()
    if(muxA == 0 and muxB == 0):
        return 0
    elif (muxA == 1 and muxB == 0):
        return 1
    elif (muxA == 0 and muxB == 1):
        return 2

def getColumn():
   for column in range(buttons_total_columns):
       if(button_column_pins[column].value() == 1):
           return column
        
def getPressedButton():
    row, column = getRow, getColumn

    return row, column


#LEDS SETUP

leds_total_rows = 4
leds_total_columns = 5

redColumn = 3
blueColumn = 4
#LAST 2 columns are RED and BLUE
led_column_pins=[Pin(12, Pin.OUT), Pin(13, Pin.OUT),Pin(25, Pin.OUT), Pin(33, Pin.OUT), Pin(32, Pin.OUT)]
led_mux_a, led_mux_b = Pin(17,Pin.OUT), Pin(23, Pin.OUT)

leds = [[Off for x in range(leds_total_columns)] for y in range(leds_total_rows) ]

print("GAME ON!")

def activate_led_row(row):
    # update multiplexer channel
    if (row == 0):
        led_mux_a.off()
        led_mux_b.off()
    elif (row == 1):
        led_mux_a.on()
        led_mux_b.off()

    elif (row == 2):
        led_mux_a.off()
        led_mux_b.on()

    elif (row == 3):
        led_mux_a.on()
        led_mux_b.on()

    for column in range(leds_total_columns):
        if(leds[row][column]):
            led_column_pins[column].on()
        else: 
            led_column_pins[column].off()


def setLed(row , col, value):
    leds[row][col] = value

def setBoardState(translated_data):
    for row, column, value in translated_data:
        setLed(row, column, value)
    
    for row, _, _ in translated_data:
        activate_led_row(row)
        sleep(0.005)


#DATA DECODING

def translate_received_box_value_to_led_columns_and_state(value):
    if value == 0:
        return [redColumn, blueColumn], Off
    if value == 1:
        return [redColumn], On
    if value == 2:
        return [blueColumn], On 

def translate_received_box_key_toRow(key):
    if (key == 1):
       return 1
    elif (key ==2):
        return 0
    elif (key == 3):
        return 3  
    elif (key == 4):
        return 2  

def translate_received_row_and_column(row, column):
    col_offset = column - 1
    if row == 1:
        return 0, col_offset if column == 2 else 0
    elif row == 2:
        return 1, col_offset
    elif row == 3:
        return 2, col_offset if column == 2 else 1
    elif row == 4:
        return 3, col_offset if column <= 2 else column - 2
    elif row == 5:
        return 3, col_offset    

def translate_received_value(value):
    if value == 1:
        return On
    else:
        return Off

def translate_received_board_state(boardStateData):
    translatedData = []
    for key, value in boardStateData.items():
        if (len(key) == 2):  #THOSE ARE THE STATES OF LINES
            receivedRow = int(key[0])
            receivedColumn = int(key[1])
            row,column = translate_received_row_and_column(receivedRow, receivedColumn)
            val = translate_received_value(value)
            translatedData.append((row, column, value))
        elif (len(key) == 1): #THOSE ARE THE STATES OF THE GRID BOXES
            intKey = int(key)
            translatedBoxRow = translate_received_box_key_toRow(intKey)
            columnToUpdate, val = translate_received_box_value_to_led_columns_and_state(value)
            for col in columnToUpdate:
                translatedData.append((translatedBoxRow, col, val))    
    return translatedData


###SERVER CONNECTION

receiver_ip = '192.168.84.33' 
server_port = 88

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Elenas', '1234567890')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()




def make_request(endpoint):
    try:
        response = urequests.get(endpoint)
        print("Response code:", response.status_code)
        print("Response text:", response.text)
        decoded_data = ujson.loads(response.text)
        print ("decoded Data", decoded_data)
    except Exception as e:
        print("Error:", e)
    finally:
        if response:
            response.close()

# Example usage
endpoint_url = "https://ubicom-team-work-898e5w4rh-liviaanapascus-projects.vercel.app/test"
make_request(endpoint_url)



# Establish a socket connection with the server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((receiver_ip, server_port))
# print('Connected to the server at')

# testJson_string =  '{"1": 0, "11": 0, "12": 0, "2": 0,
#  "21": 0, "23": 0, "3": 0, "31": 0, "32": 0, "4": 0
#  , "41": 0, "43": 0, "5": 0, "51": 0, "52": 0}'

# while True:
#     rowButton, colButton =  getPressedButton()
#     buttonPressed = str(rowButton) + str(colButton)

#     gameBoardState = client_socket.recv(1024).decode('utf-8')
#     # Decode the received JSON data
#     decoded_data = ujson.loads(gameBoardState)


















