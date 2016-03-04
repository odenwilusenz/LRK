import spidev
import RPi.GPIO as GPIO

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
SPImaj = 0 
SPImin = 0
SPIspeed = 8000000

class LRK():
  def __init__(self):
    self.spi = spidev.SpiDev()
    return

  def __enter__(self):
    self.spi.open(SPImaj, SPImin)
    self.spi.max_speed_hz = SPIspeed
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IRQ_Pin, GPIO.IN)
    GPIO.setup(CE_Pin, GPIO.OUT, initial=GPIO.LOW)
    self.clearIRQs()
    self.flushFifos()
    self.setChannel(2)
    self.setRetry(0,3)
    self.writeReg(0x00,[0x0A])
    return self

  def __exit__(self,et,ev,tb):
    self.writeReg(0x00,[0x08])
    GPIO.cleanup()
    self.spi.close()
    return


  def status(self):
    return self.spi.xfer([0xFF])[0]

  def pendingIRQ(self):
    return not(GPIO.input(IRQ_Pin))

  def readReg(self, reg, len):
    request = [reg&0x1F] + [0x00] * len
    return self.spi.xfer(request)[1:]

  def writeReg(self, reg, vals):
    self.spi.xfer([reg&0x1F|0x20] + vals)
    return

  def readPayload(self, len):
    request = [0x61] + [0x00] * len
    return self.spi.xfer(request)[1:]
    
  def writePayload(self, vals):
    self.spi.xfer([0xA0] + vals)
    return

  def writePayloadNoAck(self, vals):
    self.spi.xfer([0xB0] + vals)
    return

  def reusePayload(self):
    self.spi.xfer([0xE3])
    return

  def enableNoAck(self):
    self.writeReg(0x1D, [0x01])
    return


  def flushFifos(self):
    self.spi.xfer([0xE1])
    self.spi.xfer([0xE2])
    return

  def clearIRQs(self):
    self.writeReg(0x07,[0x70])
    return

  def setRetry(self, interval, count):
    self.writeReg(0x04, [((interval&0x0F)<<4)|count&0x0F])
    return

  def setChannel(self, chan):
    self.writeReg(0x05,[chan&0x7F])
    return

  def setAddress(self, row, place):
    self.writeReg(0x10,[0xE7,row,place,0xE7,0xE7])
    self.writeReg(0x0A,[0xE7,row,place,0xE7,0xE7])
    return

  def setColour(self, r1, g1, b1, r2, g2, b2, ack=True, calibration=True):
    pl = pwmlist(r1, g1, b1, r2, g2, b2, calibration)
    if (ack):
      self.writePayload(pl)
    else:
      self.writePayloadNoAck(pl)
    return

  def send(self):
    GPIO.output(CE_Pin, True)
    GPIO.output(CE_Pin, False)
    GPIO.wait_for_edge(IRQ_Pin, GPIO.FALLING, timeout=100)
    if (self.status()&0x10):
      self.clearIRQs()
      self.flushFifos()
      return False
    else:
      self.clearIRQs()
      return True

  def do(self, row, place, r1, g1, b1, r2, g2, b2, ack=True, calibration=True):
    self.setAddress(row, place)
    self.setColour(r1, g1, b1, r2, g2, b2, ack, calibration)
    return self.send()


def pwmlist(r1, g1, b1, r2, g2, b2, calibration):
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

