""" Defines the BOARD class that contains the board pin mappings and RF module HF/LF info. """
# -*- coding: utf-8 -*-

# Copyright 2015-2018 Mayer Analytics Ltd. and Rui Silva, 2019 THIEprojects and Werner Thie
#
# This file is part of the work bringing a Python level driver based on rpsreal/pySX127x to the ESP32 and MicroPython.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x and its derivative work for the ESP32 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU Affero General Public License for more details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

import time

from SX127x.constants import *

from machine import SPI
from machine import Pin

class BOARD:
    #Board initialisation/teardown and pin configuration is kept here.
    #TTGO LoRa seems to use either 1276/1277/1279 contrary to claiming on their
    #pinout image that it's a 1278 because the 1278 has a different frequency
    #range 137-525MHz than the others 137-1020MHz (1266/77) 137-960MHz (1279)
    #
    #Pinout of the package named U22 in the schematic
    #                        ____________________________
    #                       |                            |
    #          ANT--------16|ANT    Semtec SX1279     GND|01--------GND
    #          GND--------15|GND                  SDN/IO5|02----
    #                 ----14|IO3/RX                 RESET|03--------IO23
    #                 ----13|IO4/TX               NSS/SEL|04--------IO18
    #       VCC3V3--------12|VCC/3V3                  SCK|05--------IO05
    #         IO26--------11|IO0                 MOSI/SDI|06--------IO27
    #       HPDIO1--------10|IO1                 MISO/SDO|07--------IO19
    #       HPDIO2--------09|IO2                      GND|08--------GND
    #                       |____________________________|                       
    #
    #SPI documentation http://docs.micropython.org/en/latest/library/pyb.SPI.html

    DIO0 = Pin(26, mode=Pin.IN) #only have this wired on the ESP32 LoRa board
    DIO1 = -1
    DIO2 = -1
    DIO3 = -1
    
    RST  = Pin(23, mode=Pin.OUT, value=1)  #reset signal force high   
    NSS  = Pin(18, mode=Pin.OUT, value=1)  #the CS signal in another abreviation, force high
    
    # The spi object is kept here
    spi = None
    
    SCK  = Pin(5, mode=Pin.OUT)
    MOSI = Pin(27,mode=Pin.OUT) 
    MISO = Pin(19,mode=Pin.IN)
    
    # tell pySX127x here whether the attached RF module uses low-band (RF*_LF pins) or high-band (RF*_HF pins).
    # low band (called band 1&2) are 137-175 and 410-525
    # high band (called band 3) is 862-1020
    low_band = False

    @staticmethod
    def setup():
      BOARD.reset()
      BOARD.mode = MODE.SLEEP
      return BOARD.xfer([REG.LORA.OP_MODE | 0x80, BOARD.mode])[1]
   
    @staticmethod
    def teardown():
      BOARD.spi.deinit()

    @staticmethod
    def createSPI():
      BOARD.spi = SPI(1, baudrate=5000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=BOARD.SCK, mosi=BOARD.MOSI, miso=BOARD.MISO)
      return BOARD.spi

    @staticmethod
    def xfer(wbuf):
      BOARD.NSS.value(0)
      rbuf = bytearray([0] * len(wbuf))            #make rbuf the same size as wbuf
      BOARD.spi.write_readinto(bytearray(wbuf), rbuf)
      BOARD.NSS.value(1)
      return list(rbuf)
    
    @staticmethod
    def add_event(apin, callback):
      apin.irq(handler=callback, trigger=Pin.IRQ_RISING)

    @staticmethod
    def add_events(cb_dio0, cb_dio1, cb_dio2, cb_dio3, cb_dio4, cb_dio5, switch_cb=None):
      BOARD.add_event(BOARD.DIO0, callback=cb_dio0) #only have this wired on the ESP32 LoRa board
      #BOARD.add_event_detect(BOARD.DIO1, callback=cb_dio1)x
      #BOARD.add_event_detect(BOARD.DIO2, callback=cb_dio2)
      #BOARD.add_event_detect(BOARD.DIO3, callback=cb_dio3)

    @staticmethod
    def led_on(value=1):
      return value

    @staticmethod
    def led_off():
      return 0
    
    @staticmethod
    def reset():
      BOARD.RST.value(0)
      time.sleep_ms(10)
      BOARD.RST.value(1)
      time.sleep_ms(10)
      return 0

    @staticmethod
    def blink(time_sec, n_blink):
      pass

def main():
  pass

if __name__ == "__main__":
  print('...running main')
  main()

