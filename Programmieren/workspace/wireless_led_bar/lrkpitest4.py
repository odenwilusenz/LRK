import lrkpimaster
import sys
import time

addressMap = [1,3,5,7,9,11,15,17,19,21,23,25]

with lrkpimaster.LRK() as lrk:
  lrk.setRetry(15,15)
  lrk.enableNoAck()
  packets = 0
  resent = 0
  lost = 0
  row = int(sys.argv[1]) % 256
  place = 0
  while True:
    place = 0
    resent = 0
    lost = 0
    starttime = time.time()
    for _ in range(12):
#      if (not(lrk.do(row, addressMap[place],55,55,55,55,55,55))):
      lrk.setAddress(row, addressMap[place])
      lrk.writePayloadNoAck([249, 12, 251, 3, 1, 0, 1, 0, 1, 245, 6, 1, 0, 1])
      if (not(lrk.send())):
        lost += 1
      resent += lrk.readReg(8,1)[0]&0x0F
      place += 1
    stoptime = time.time()
    print ('sent: 12 - resent: '+str(resent)+'('+str((100*resent)/12)+'%) - lost: '+str(lost)+'('+str((100*lost)/12)+'%) - time: '+str(stoptime-starttime)+'s')

