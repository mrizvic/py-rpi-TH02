import TH02_module as TH02
from time import sleep

def main():
    TH02.init_io()
    while True:
        print("----------------------------")
        print("Temperatura je: " + str(TH02.get_temp()))
        print("Relativna vlaznost je: " + str(TH02.get_humi()))
        sleep(1)
main()

