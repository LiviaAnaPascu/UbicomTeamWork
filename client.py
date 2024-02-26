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

# testJson_string =  '{"1": 2, "11": 0, "12": 0, "2": 0,
#  "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 1
#  , "41": 0, "42":0, "43": 0, "51": 0, "52": 0}'

from machine import Pin
from time import sleep
import ujson
import usocket as socket
import network
import urequests


Off, On, isPressed, NotPressed = False, True, True, False

#BUTTONS SETUP
buttons_total_rows = 4
buttons_total_columns = 3

button_column_pins = [Pin(36, Pin.IN), Pin(37, Pin.IN), Pin(38, Pin.IN)]
button_mux_a, button_mux_b = Pin(34, Pin.IN), Pin(35, Pin.IN)

buttons = [[NotPressed for _ in range(buttons_total_columns)] for _ in range(buttons_total_rows)]
print("Buttons", buttons)

def getRow(): 
    muxA = button_mux_a.value()
    muxB = button_mux_b.value()
    if(muxA == 0 and muxB == 0):
        return 0
    elif (muxA == 1 and muxB == 0):
        return 1
    elif (muxA == 0 and muxB == 1):
        return 2
    elif (muxA == 0 and muxB == 1):
        return 3

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
led_column_pins=[Pin(22, Pin.OUT), Pin(23, Pin.OUT),Pin(2, Pin.OUT), Pin(17, Pin.OUT), Pin(32, Pin.OUT)]
led_mux_a, led_mux_b = Pin(12,Pin.OUT), Pin(13, Pin.OUT)

leds = [[Off for x in range(leds_total_columns)] for y in range(leds_total_rows) ]

led_mux_a.off()
led_mux_b.off()
for col in led_column_pins:
    col.off()


print("LEDS", leds)
print("GAME ON!")

def activate_mux_channel(row):
    if (row == 1):
        led_mux_a.off()
        led_mux_b.off()
    elif (row == 2):
        led_mux_a.on()
        led_mux_b.off()
    elif (row == 3):
        led_mux_a.off()
        led_mux_b.on()
    elif (row == 0):
        led_mux_a.on()
        led_mux_b.on()


def activate_row(row, begin = 0, end = leds_total_columns):
    activate_mux_channel(row)
    # update column pins
    for column in range(leds_total_columns):
        if leds[row][column] and column >= begin and column < end:
            led_column_pins[column].on()
        else:
            led_column_pins[column].off()


current_led_row = 0

def led_update():
    global current_led_row
    #print(current_led_row)
    if current_led_row < leds_total_rows:
        activate_row(current_led_row, 0, 3)
        print(current_led_row)
        sleep(0.001)
    else:
        pass
        # activate_row(current_led_row % leds_total_rows, 3, 5)
    current_led_row = (current_led_row + 1) % (leds_total_rows * 2)

def setLed(row , col, value):
    leds[row][col] = value

def setBoardState(translated_data):
    for ledState in translated_data:
        row, column, value = ledState
        print(ledState)
       # setLed(row, column, value)

activate_mux_channel(0)
led_column_pins[0].on()



#DATA DECODING

def translate_received_box_value_to_led_columns_and_state(value):
    if value == 0:
        return [(redColumn, Off),(blueColumn, Off)]
    if value == 1:
        return [(redColumn, On), (blueColumn, Off)]
    if value == 2:
        return [(blueColumn, On), (redColumn, Off)] 

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
    #'{"1": 0, "11": 0, "12": 0, "2": 0, "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 0 , "41": 0, "42":1, "43": 0, "51": 0, "52": 0}'
    #((0,0) (0,2), (1,0),(0,1))
    if row == 1:
        if column == 1:
          return 0,0
        elif column == 2:
          return 0,2
    elif row == 2:
        if column == 1:
            return 1,0
        elif column == 2:
            return 0,1
        elif column == 3:
            return 1,2
    elif row == 3:
        if column == 1:
            return 2,0
        elif column == 2:
            return 1,1
    elif row == 4:
        if column == 1:
            return 3,0
        elif column == 2:
            return 2,1
        elif column == 3:
            return 2,2
    elif row == 5:
        if column == 1:
            return 3,1
        elif column == 2:
            return 3,2   

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
            translatedData.append((row, column, val))
        elif (len(key) == 1): #THOSE ARE THE STATES OF THE GRID BOXES
            intKey = int(key)
            translatedBoxRow = translate_received_box_key_toRow(intKey)
            columnToUpdate = translate_received_box_value_to_led_columns_and_state(value)
            for columnAndValue in columnToUpdate:
                col, val = columnAndValue
                translatedData.append((translatedBoxRow, col, val))    
    return translatedData


###SERVER CONNECTION

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

translatedData = []

def request_board_state(endpoint):
    try:
        response = urequests.get(endpoint)
        print("Response:", response)
        json_data =response.json()
        print("Response JSON:", '{"1": 0, "11": 0, "12": 0, "2": 0, "21": 0,"22": 1,"23": 0, "3": 0, "31": 0, "32": 0, "4": 0 , "41": 0, "42":1, "43": 0, "51": 0, "52": 0}')
        translatedData = translate_received_board_state(json_data)
        setBoardState(translatedData)
        print("Translated data:", translatedData)
        #print(ujson.dumps(json_data, indent=2))
    except Exception as e:
        print("Error:", e)
    finally:
        if response:
            response.close()

# Example usage
endpoint_url = "https://ubicom-team-work-seven.vercel.app/test"
request_board_state(endpoint_url)
print("NEW LEDS",leds)

# while True:
#     led_update()


# while True: 
#     sleep(1)













