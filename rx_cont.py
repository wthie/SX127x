import sys, time

from SX127x.constants import *

from SX127x.LoRa import LoRa

class LoRaRcvCont(LoRa):
  def __init__(self, verbose=False):
    super(LoRaRcvCont, self).__init__(verbose)
    self.set_dio_mapping([0] * 6)

  def on_rx_done(self):
    print("\nrx_done")
    self.clear_irq_flags(rx_done=1)
    payload = self.read_payload(nocheck=True)
    print(payload)
    self.set_mode(MODE.SLEEP)
    self.reset_ptr_rx()
    self.set_mode(MODE.RXCONT)

  def on_tx_done(self):
    print("\nTxDone")
    print(self.get_irq_flags())

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
    self.reset_ptr_rx()
    self.set_mode(MODE.RXCONT)
    while True:
      time.sleep(.5)
      rssi_value = self.get_rssi_value()
      status = self.get_modem_status()
      sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))

  def stop(self):
    self.board.teardown()
    print('...SPI again disconnected')

def main():
  lora = LoRaRcvCont(verbose=False)
  print('LoRa object created')
  
  ret = lora.set_mode(MODE.STDBY)
  print('LoRa set mode stand by', ret)

  ret = lora.set_freq(915.0)
  print('LoRa set_freq', ret)
  
  ret = lora.set_pa_config(pa_select=1)
  print('LoRa set pa_select', ret)
  
  ret = lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
  print('LoRa set pa_ramp', ret)
  
  ret = lora.set_pa_config(max_power=0, output_power=0)
  print('LoRa set pa_config', ret)

  ret = lora.set_rx_crc(True)
  print('LoRa set rx_crc', ret)

  ret = lora.set_coding_rate(CODING_RATE.CR4_6)
  print('LoRa set coding rate', ret)

  ret = lora.set_lna_gain(GAIN.G1)
  print('LoRa set lna_gain', ret)

  ret = lora.set_low_data_rate_optim(True)
  print('LoRa set low_data_rate_optim', ret)
  
  ret = lora.set_implicit_header_mode(False)
  print('LoRa set implicit_header_mode', ret)

  ret = lora.set_agc_auto_on(True)
  print('LoRa set agc_auto_on', ret)
  
  #lora.stop()
  #sys.exit(0)
  
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
  
