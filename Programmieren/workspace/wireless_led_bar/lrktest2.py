import lrkmaster
import sys
import random
import time

with lrkmaster.LRKmaster(sys.argv[1]) as lrk:
  packets = 0
  resent = 0
  lost = 0
  row = int(sys.argv[2]) % 256
  place = int(sys.argv[3]) % 256
  c = [0,0,0,0,0,0] 
  cc = [0,0,0,0,0,0]
  while True:
    cc = map(lambda x: random.randint(-1,1), cc)
    for _ in range(64):
      packets += 1
      try:
        lrk.do(row, place, abs(c[0])%256,abs(c[1])%256,abs(c[2])%256,abs(c[3])%256,abs(c[4])%256,abs(c[5])%256)
      except lrkmaster.LRKError:
        lost += 1
      resendReg = int('0x'+lrk.readReg(8),16)
      plos = resendReg >> 4
      arc = resendReg & 0x0F
      resent += arc

      for i in range(6):
        c[i] = c[i]+random.randint(-1,1)+cc[i]
        if (c[i] > 255):
          c[i] = 255
        if (c[i] < -255):
          c[i] = -255
        time.sleep(0.005)
    print 'packets sent: '+str(packets)+' - packets resent: '+str(resent)+'('+str((100*resent)/packets)+'%) - packets lost: '+str(lost)+'('+str((100*lost)/packets)+'%)'

