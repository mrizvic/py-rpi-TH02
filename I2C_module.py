#spreminjanje SDA je v casu SCL nizkega nivoja
#branje SDA ob pozitivni foronti SCL

#start_bit: SCL visok nivo, SDA iz visokega v nizek nivo
#stop_bit: SCL visok nivo, SDA iz nizkega v visoko

#zadnjega Byte-a se ne potrjuje - nack, vse ostale pa - ack

import RPi.GPIO as GPIO
from time import sleep 

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# pini za komunikacijo in ostale spremenljivke
_I2C_sda = 3
_I2C_scl = 5
delay = 0.000010 #10 usec

def version():
    return "Version 1.0"

def set_io(sda_pin = 3, scl_pin = 5):
    if sda_pin < 1 or sda_pin > 26:
        raise ValueError("Serial data pin '" + str(sda_pin) + "' is out of range!")
    if scl_pin < 1 or scl_pin > 26:
        raise ValueError("Serial clock pin '" + str(scl_pin) + "' is out of range!")
    _I2C_sda = sda_pin
    _I2C_scl = scl_pin

def init_io():
    GPIO.setup(_I2C_sda, GPIO.OUT)
    GPIO.setup(_I2C_scl, GPIO.OUT)

def start_bit():
    """Write bits to the I2C line for start_bit the transmit"""
    GPIO.output(_I2C_sda, True)
    sleep(delay)
    GPIO.output(_I2C_scl, True)
    sleep(delay)
    GPIO.output(_I2C_sda, False)
    sleep(delay)
    GPIO.output(_I2C_scl, False)
    sleep(delay)

def stop_bit():
    GPIO.output(_I2C_scl, False)
    sleep(delay)
    GPIO.output(_I2C_sda, False)
    sleep(delay)
    GPIO.output(_I2C_scl, True)
    sleep(delay)
    GPIO.output(_I2C_sda, True)
    sleep(delay)
    
def ack():
    GPIO.output(_I2C_scl, False)     #tega ni v C kodi
    sleep(delay)                    #tega ni v C kodi
    GPIO.output(_I2C_sda, False)
    sleep(delay)
    GPIO.output(_I2C_scl, True)
    sleep(delay)
    GPIO.output(_I2C_scl, False)
    sleep(delay)

def nack():
    GPIO.output(_I2C_scl, False)     #tega ni v C kodi
    sleep(delay)                    #tega ni v C kodi
    GPIO.output(_I2C_sda, True)
    sleep(delay)
    GPIO.output(_I2C_scl, True)
    sleep(delay)
    GPIO.output(_I2C_scl, False)
    sleep(delay)    

def read_byte():
    GPIO.setup(_I2C_sda, GPIO.IN)
    vrednost = 0
    for j in range (8):
        vrednost = vrednost << 1
        GPIO.output(_I2C_scl, False)
        sleep(delay)
        GPIO.output(_I2C_scl, True)
        sleep(delay)
#        print("\"read_byte\" - tren. preb.:", GPIO.input(_I2C_sda))
        if GPIO.input(_I2C_sda):
            #shranimo vrednost 1 na zadnje mesto
            vrednost = vrednost | 1
        sleep(delay)
        GPIO.output(_I2C_scl, False)
        sleep(delay)
    GPIO.setup(_I2C_sda, GPIO.OUT)
#    print("\"read_byte\" - tren. vr. 'vrednost':", vrednost)
    return vrednost

def write_byte(data):
    """Write one Byte to the I2C line"""
    if not (data > 0x00 or data < 0xFF):
        raise ValueError("Given 'data' argument (" + str(data) + ")is not byte")
    data = bin(data)
    data = data[2:]

    while len(data) < 8:
        data = "0"+data

    for i in data:
        #print(str(i))
        bit = int(i)
        GPIO.output(_I2C_scl, False) #ta in naslednja vrstica nj bi sle pred for loop
        sleep(delay)
        GPIO.output(_I2C_sda, bit)
        sleep(delay)
        GPIO.output(_I2C_scl, True) #branje ob pozitivni fronti
        sleep(delay)
        GPIO.output(_I2C_scl, False)
        sleep(delay)

    GPIO.setup(_I2C_sda, GPIO.IN)
    sleep(delay)
    
    GPIO.output(_I2C_scl, False)
    sleep(delay)
    GPIO.output(_I2C_scl, True)
    #tu bi mogu prevert, ce je slave poul_down-al SDA linijo
    sleep(delay)
    GPIO.output(_I2C_scl, False)
    sleep(delay)
    
    GPIO.setup(_I2C_sda, GPIO.OUT)

def write_message_byte(chip_address, data_address, data):
    """Send byte to selected chip to selected address"""
    if(chip_address < 0 or chip_address > 0xFF):
        #raise WrongChipAddressError(("Chip address " + str(chip_address) + " is out of range"))
        raise ValueError(("Chip address '" + str(chip_address) + "' is out of range!"))
        #pass #TODO vrzi izjemo
    ch_addr = chip_address << 1  #dodamo bit za pisanje
    start_bit()
    write_byte(ch_addr)
    if data_address is not -1:
        write_byte(data_address)
    write_byte(data)
    stop_bit()

def read_mssage_word(chip_address, data_address):
    pass

def main():
    #send_message_byte(-1, 0x02, 0x22)
    pass

if __name__ == "__main__":
    try:
        main()
    except:
        print("Caught Exception!")
        raise
    finally:
        GPIO.cleanup()


