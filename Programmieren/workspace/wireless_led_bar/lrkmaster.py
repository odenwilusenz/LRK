import serial
import time

B1mask = 0b00000001
B2mask = 0b00000010
G1mask = 0b00000100
G2mask = 0b00001000
R1mask = 0b00000010
R2mask = 0b00000100

class LRKError(Exception):
  pass

class LRKmaster:
  def __init__(self, portname):
    self.portname = portname
    self.lastaddress = (231,231)
    self.lastcolour = (0,0,0,0,0,0)
    return

  def __enter__(self):
    self.ser = serial.Serial(self.portname, 9600, timeout=1)
    time.sleep(2)
    self.ser.flushInput()
    self.ser.flushOutput()
    try:
      self.hello()
      self.flushFifos()
      self.address(231,231)
      self.colour(0,0,0,0,0,0)
    except:
      self.ser.close()
      raise
    return self

  def __exit__(self, et,ev,tb):
    if (et == None and ev == None and tb == None):
      self.ser.write(b'q')
      self.ser.write(b'a231,231,231,231,231.')
      self.ser.write(b'b0,0,0,0,0,0,0,0,0,0,0,0,0,0.')
      self.ser.flushInput()
    self.ser.close()
    return

  def hello(self):
    self.ser.write(b'h')
    hello = str.strip(self.ser.readline())
    if (hello != '1.1ok'):
      raise LRKError('device identification failed. device returned ', hello, ' instead of 1.0ok')
    return

  def status(self):
    self.ser.write(b's')
    return str.strip(self.ser.readline())

  def flushFifos(self):
    self.ser.write(b'f')
    if (str.strip(self.ser.readline()) != 'ok'):
      raise LRKError('flushing fifos failed')
    return

  def clearInterrupts(self):
    self.ser.write(b'q')
    if (str.strip(self.ser.readline()) != 'ok'):
      raise LRKError('clearing interrupts failed')
    return

  def channel(self, chan):
    self.ser.write(b'c')
    self.ser.write(str(int(chan) % 256))
    self.ser.write(b'.')
    if (str.strip(self.ser.readline()) != 'ok'):
      raise LRKError('setting channel failed')
    return

  def address(self, row, place):
    rowstring = str(int(row) % 256)
    placestring = str(int(place) % 256)
    self.ser.write(b'a231,')
    self.ser.write(rowstring)
    self.ser.write(b',')
    self.ser.write(placestring)
    self.ser.write(',231,231.')
    if (str.strip(self.ser.readline()) != 'ok'):
      raise LRKError('setting send address failed')
    self.lastaddress = (row,place)
    return

  def colour(self, r1, g1, b1, r2, g2, b2):
    pl = pwmlist(r1, g1, b1, r2, g2, b2)
    self.ser.write(b'b')
    for v in pl[:-1]:
      self.ser.write(str(v))
      self.ser.write(b',')
    self.ser.write(b'1.')
    if (str.strip(self.ser.readline()) != 'ok'):
       raise LRKError('setting pwmlist buffer failed')
    self.lastcolour = (r1, g1, b1, r2, g2, b2)
    return

  def send(self):
    self.ser.write(b't')
    if (str.strip(self.ser.readline()) != 'ok'):
       raise LRKError('sending failed')
    return

  def do(self, row, place, r1, g1, b1, r2, g2, b2):
    if (self.lastaddress != (row, place)):
      self.address(row, place)
    if (self.lastcolour != (r1, g1, b1, r2, g2, b2)):
      self.colour(r1, g1, b1, r2, g2, b2)
    self.send()
    return


def pwmlist(r1, g1, b1, r2, g2, b2):
  pwmlistbg =[1,0,1,0,1,0,1,0,1] 
  pwmlistr = [1,0,1,0,1]
  basebg = [(int(b1),B1mask),(int(b2),B2mask),(int(g1),G1mask),(int(g2),G2mask)]
  baser = [(int(r1),R1mask),(int(r2),R2mask)]
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
