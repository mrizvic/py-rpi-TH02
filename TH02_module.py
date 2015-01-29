import I2C_module as I2C
from time import sleep

#delay = 0.000010 #10 usec
rdy_check_delay = 0.025

def set_io(sda_pin = 3, scl_pin = 5):
    I2C.set_io(sda_pin, scl_pin)
    
def init_io():
    I2C.init_io()

def convert_temp(): #povprecno pretvorba traja 35ms
    """Send command to TH02 for convert temprerature"""
    #zahteva za pretvorbo temperature
    #I2C.start_bit()
    #I2C.write_byte(0x80) #0x40 + write bit
    #I2C.write_byte(0x03) #naslovljen register 0x03
    #I2C.write_byte(0x11) #pisemo 0x11 temp, 0x01 humi
    #I2C.stop_bit()
    I2C.write_message_byte(0x40, 0x03, 0x11)
    

def convert_humi(): #povprecno pretvorba traja 35ms
    """Send command to TH02 for convert humidity"""
    #zahteva za pretvorbo temperature
    #I2C.start_bit()
    #I2C.write_byte(0x80) #0x40 + write bit
    #I2C.write_byte(0x03) #naslovljen register 0x03
    #I2C.write_byte(0x01) #pisemo 0x11 temp, 0x01 humi
    #I2C.stop_bit()
    I2C.write_message_byte(0x40, 0x03, 0x01)

def is_rdy(): #je pretvorba, ki povprecno traja 35ms, ze koncana
    """Is sensor done with convertation"""
    I2C.start_bit()
    I2C.write_byte(0x80)
    I2C.write_byte(0x00)
    I2C.start_bit()
    I2C.write_byte(0x81)
    tmp_rdy = I2C.read_byte()
    I2C.nack()
    I2C.stop_bit()
    if not tmp_rdy: #'0' pretvorba koncana, '1' pretvorba v teku
        return True
    else:
        return False

def _read_temp_humi():
    """Read the 0x01 & 0x02 register value"""
    #branje temperature iz TH02
    I2C.start_bit()
    I2C.write_byte(0x80) #0x40 + write bit
    I2C.write_byte(0x01) #naslovljen register 0x01
    I2C.start_bit() #ponoven start bit, ker bomo brali
    I2C.write_byte(0x81) #0x40 + read bit
    tmp_temp_humi = I2C.read_byte()
    I2C.ack() #prvi Byte potrdimo
    tmp_temp_humi = tmp_temp_humi << 8
    tmp_temp_humi = tmp_temp_humi | I2C.read_byte()
    I2C.nack() #zadnjega Byte-a ne potrdimo
    I2C.stop_bit()
    return tmp_temp_humi

def calc_temp():
    """Calculate temperature from readed data."""
    temp = _read_temp_humi()
    temp = temp >> 2
    temp /= 32
    temp -= 50
    return temp

def calc_humi():
    """Calculate humidity from readed data."""
    humi = _read_temp_humi()
    humi = humi >> 4
    humi /= 16
    humi -= 24
    return humi
    
def get_temp():
    """Return temperature or -60 if there is an error"""
    convert_temp()
    sleep(0.040) #povprecno pretvorba traja 35ms
    for i in range (2): #ce pretvorba se ni koncana, cez 30 ms preverimo se enkrat
        if is_rdy():
            return calc_temp()
        else:
            sleep(0.03)
    return -60 #"Conversion not possible"
               
def get_humi():
    """Return relativ humiditi or -60 if there is an error"""
    convert_humi()
    sleep(0.040) #povprecno pretvorba traja 35ms
    for i in range (2): #ce pretvorba se ni koncana, cez 30 ms preverimo se enkrat
        if is_rdy():
            return calc_humi()
        else:
            sleep(0.03)
    return -60 #"Conversion not possible"
            
def main():
    init_io()
    print(get_temp())
    print(get_humi())
    
    
    #print("\"main\" - v st. cel.:", prebrano_main/32-50)






if __name__ == "__main__":
    try:
        main()
    except:
        print("Caught Exception!")
        raise
    finally:
        pass
        I2C.GPIO.cleanup()

