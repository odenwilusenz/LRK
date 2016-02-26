import lrkpimaster
import sys
import random
import time

addressMap = [1,3,5,7,9,11,15,17,19,21,23,25]

with lrkpimaster.LRK() as lrk:
  lrk.setRetry(15,15)
  packets = 0
  resent = 0
  lost = 0
  place = 0
  timestamp = 0
  row = int(sys.argv[1]) % 256
  c = [0,0,0,0,0,0] 
  cc = [0,0,0,0,0,0]
  while True:
    cc = list(map(lambda x: random.randint(-1,1), cc))
    packets = 0
    resent = 0
    lost = 0
    place = 0
    timestamp = time.time()
    for _ in range(12):
      packets += 1
      if (not(lrk.do(row, addressMap[place], abs(c[0])%256,abs(c[1])%256,abs(c[2])%256,abs(c[3])%256,abs(c[4])%256,abs(c[5])%256))):
        lost += 1
      resendReg = lrk.readReg(8,1)[0]
      plos = resendReg >> 4
      arc = resendReg & 0x0F
      resent += arc
      place += 1

      for i in range(6):
        c[i] = c[i]+random.randint(-1,1)+cc[i]
        if (c[i] > 255):
          c[i] = 255
        if (c[i] < -255):
          c[i] = -255
    print ('sent: '+str(packets)+' - resent: '+str(resent)+'('+str((100*resent)/packets)+'%) - lost: '+str(lost)+'('+str((100*lost)/packets)+'%) - time: '+str(time.time()-timestamp)+'s')

