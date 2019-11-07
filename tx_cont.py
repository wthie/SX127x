""" A simple continuous transmitter class. """

# Copyright 2019 THIEprojects
#
# This file is part of SX127x package which was ported from pySX127x by THIEprojects to the ESP32 microPython implementation
#
# pySX127x and the ported SX127x package is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# SX127x package is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

import sys, time

from SX127x.constants import *

from SX127x.LoRa import LoRa

class LoRaTxCont(LoRa):

  tx_counter = 0

  def __init__(self, verbose=False):
    super(LoRaTxCont, self).__init__(verbose)
    self.set_dio_mapping([1,0,0,0,0,0])

  def on_rx_done(self):
    print("\nRxDone")
    print(self.get_irq_flags())
    print(map(hex, self.read_payload(nocheck=True)))
    self.set_mode(MODE.SLEEP)
    self.reset_ptr_rx()
    self.set_mode(MODE.RXCONT)

  def on_tx_done(self):
    self.set_mode(MODE.STDBY)
    self.clear_irq_flags(tx_done=1)
    self.tx_counter += 1
    sys.stdout.write("\rtx #%d" % self.tx_counter)

  def on_cad_done(self):
    print("\non_CadDone")
    print(self.get_irq_flags())

  def on_rx_timeout(self):
    print("\non_RxTimeout")
    print(self.get_irq_flags())

  def on_valid_header(self):
    print("\non_ValidHeader")
    print(self.get_irq_flags())

  def on_payload_crc_error(self):
    print("\non_PayloadCrcError")
    print(self.get_irq_flags())

  def on_fhss_change_channel(self):
    print("\non_FhssChangeChannel")
    print(self.get_irq_flags())

  def start(self):
    sys.stdout.write("\rstart")
    self.tx_counter = 0
    while True:
      time.sleep(1)
      self.write_payload([0x0f])
      self.set_mode(MODE.TX)

  def stop(self):
    self.board.teardown()
    print('...SPI again disconnected')

def main():
  lora = LoRaTxCont(verbose=False)
  
  ret = lora.set_freq(915.0)
  #print('LoRa set_freq', ret)
  
  ret = lora.set_mode(MODE.STDBY)
  #print('LoRa set mode stand by', ret)

  ret = lora.set_pa_config(pa_select=1)
  #print('LoRa set pa_select', ret)
  
  ret = lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
  #print('LoRa set pa_ramp', ret)
  
  ret = lora.set_pa_config(max_power=0, output_power=0)
  #print('LoRa set pa_config', ret)

  print()
  print('------------------------------------')
  print(lora)
  
  assert(lora.get_agc_auto_on() == 1)
  try:
    lora.start()
  except KeyboardInterrupt:
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
  finally:
    print("")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    lora.stop()
    
    
if __name__ == "__main__":
  main()
  

