import lrkpimaster
import random
import time

addressMap = [[1,1],[1,3],[1,5],[1,7],[1,9],[1,11],[1,15],[1,17],[1,19],[1,21],[1,23],[1,25],
              [2,1],[2,3],[2,5],[2,7],[2,9],[2,11],[2,15],[2,17],[2,19],[2,21],[2,23],[2,25],
              [3,1],[3,3],[3,5],[3,7],[3,9],[3,11],[3,15],[3,17],[3,19],[3,21],[3,23],[3,25],
              [4,1],[4,3],[4,5],[4,7],[4,9],[4,11],[4,15],[4,17],[4,19],[4,21],[4,23],[4,25],
              [5,1],[5,3],[5,5],[5,7],[5,9],[5,11],[5,15],[5,17],[5,19],[5,21],[5,23],[5,25]]


def cc(c):
 if (c > 255):
   return -255
 else:
   return c+1
  

with lrkpimaster.LRK() as lrk:
  lrk.setRetry(3,3)
  lrk.enableNoAck()
  packets = 0
  resent = 0
  lost = 0
  place = 0
  timestamp = 0
  c = [-255,-255,-255,-255,-255,-255] 
  while True:
    c = list(map(lambda x: cc(x), c))
    packets = 0
    resent = 0
    lost = 0
    place = 0
    timestamp = time.time()
    for addr in addressMap:
      packets += 1
      if (not(lrk.do(addr[0], addr[1], abs(c[0])%256,abs(c[1])%256,abs(c[2])%256,abs(c[3])%256,abs(c[4])%256,abs(c[5])%256, False, True))):
        lost += 1
      resendReg = lrk.readReg(8,1)[0]
      plos = resendReg >> 4
      arc = resendReg & 0x0F
      resent += arc
      place += 1
    print ('sent: '+str(packets)+' - resent: '+str(resent)+'('+str((100*resent)/packets)+'%) - lost: '+str(lost)+'('+str((100*lost)/packets)+'%) - time: '+str(time.time()-timestamp)+'s')

