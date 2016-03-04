import rpyc
import spidev
import RPi.GPIO as GPIO
from rpyc.utils.server import ThreadedServer

B1mask = 0b00000001
B2mask = 0b00000010
G1mask = 0b00000100
G2mask = 0b00001000
R1mask = 0b00000010
R2mask = 0b00000100

b_calibration = [x**2/600 for x in range(0,256)]
g_calibration = [x**2/400 for x in range(0,256)]
r_calibration = [x**2/255 for x in range(0,256)]

CE_Pin = 22
IRQ_Pin = 18

class LRKService(rpyc.Service):
  def on_connect(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0,0)
    self.spi.max_speed_hz = 5000000
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IRQ_Pin, GPIO.IN)
    GPIO.setup(CE_Pin, GPIO.OUT, initial=GPIO.LOW)
    self.exposed_clearIRQs()
    self.exposed_flushFifos()
    self.exposed_setChannel(2)
    self.exposed_setRetry(0,3)
    self.exposed_writeReg(0x00,[0x0A])
    return

  def on_disconnect(self):
    self.exposed_writeReg(0x00,[0x08])
    GPIO.cleanup()
    self.spi.close()
    return


  def exposed_status(self):
    return self.spi.xfer([0xFF])[0]

  def exposed_pendingIRQ(self):
    return not(GPIO.input(IRQ_Pin))

  def exposed_readReg(self, reg, len):
    request = [reg&0x1F] + [0x00] * len
    return self.spi.xfer(request)[1:]

  def exposed_writeReg(self, reg, val):
    self.spi.xfer([reg&0x1F|0x20] + val)
    return

  def exposed_readPayload(self, len):
    request = [0x61] + [0x00] * len
    return self.spi.xfer(request)[1:]
    
  def exposed_writePayload(self, val):
    self.spi.xfer([0xA0] + val)
    return

  def exposed_flushFifos(self):
    self.spi.xfer([0xE1])
    self.spi.xfer([0xE2])
    return

  def exposed_clearIRQs(self):
    self.exposed_writeReg(0x07,[0x70])
    return

  def exposed_setRetry(self, interval, count):
    self.exposed_writeReg(0x04, [((interval&0x0F)<<4)|count&0x0F])
    return

  def exposed_setChannel(self, chan):
    self.exposed_writeReg(0x05,[chan&0x7F])
    return

  def exposed_setAddress(self, row, place):
    self.exposed_writeReg(0x10,[0xE7,row,place,0xE7,0xE7])
    self.exposed_writeReg(0x0A,[0xE7,row,place,0xE7,0xE7])
    return

  def exposed_setColour(self, r1, g1, b1, r2, g2, b2, calibration=True):
    pl = pwmlist(r1, g1, b1, r2, g2, b2, calibration)
    self.exposed_writePayload(pl)
    return

  def exposed_send(self):
    GPIO.output(CE_Pin, True)
    GPIO.output(CE_Pin, False)
    GPIO.wait_for_edge(IRQ_Pin, GPIO.FALLING, timeout=100)
    if (self.exposed_status()&0x10):
      self.exposed_clearIRQs()
      self.exposed_flushFifos()
      return False
    else:
      self.exposed_clearIRQs()
      return True

  def exposed_do(self, row, place, r1, g1, b1, r2, g2, b2):
    self.exposed_setAddress(row, place)
    self.exposed_setColour(r1, g1, b1, r2, g2, b2)
    return self.exposed_send()


def pwmlist(r1, g1, b1, r2, g2, b2,calibration):
  pwmlistbg =[1,0,1,0,1,0,1,0,1] 
  pwmlistr = [1,0,1,0,1]
  if (calibration):
    b1c = b_calibration[b1]
    b2c = b_calibration[b2]
    g1c = g_calibration[g1]
    g2c = g_calibration[g2]
    r1c = r_calibration[r1]
    r2c = r_calibration[r2]
  else:
    b1c = b1
    b2c = b2
    g1c = g1
    g2c = g2
    r1c = r1
    r2c = r2
    
  basebg = [(int(b1c),B1mask),(int(b2c),B2mask),(int(g1c),G1mask),(int(g2c),G2mask)]
  baser = [(int(r1c),R1mask),(int(r2c),R2mask)]
  cropbg = filter(lambda a: a[0] != 0, basebg)
  cropr = filter(lambda a: a[0] != 0, baser)
  negbg = map(lambda a: (-a[0]%256,a[1]), cropbg)
  negr = map(lambda a: (-a[0]%256,a[1]), cropr)
  last = 0
  i = 0
  for a in sorted(negbg):
    if (a[0] == last):
      pwmlistbg[i*2-1] = pwmlistbg[i*2-1] | a[1]      
    else:
      pwmlistbg[i*2] = a[0]
      pwmlistbg[i*2+1] = a[1]
      last = a[0]
      i = i + 1
  last = 0
  i = 0
  for a in sorted(negr):
    if (a[0] == last):
      pwmlistr[i*2-1] = pwmlistr[i*2-1] | a[1]      
    else:
      pwmlistr[i*2] = a[0]
      pwmlistr[i*2+1] = a[1]
      last = a[0]
      i = i + 1
  return pwmlistbg+pwmlistr

if __name__ == "__main__":
  server = ThreadedServer(LRKService, hostname="localhost", port = 12345)
  server.start()
