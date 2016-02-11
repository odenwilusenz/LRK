import lrkmaster
import sys
import random
import time

addressMap = [1,3,5,7,9,11,15,17,19,21,23,25]

with lrkmaster.LRKmaster(sys.argv[1]) as lrk:
  packets = 0
  resent = 0
  lost = 0
  row = int(sys.argv[2]) % 256
  place = 0
  while True:
    place = 0
    for _ in range(12):
      packets += 1
      try:
        lrk.do(row, addressMap[place],55,55,55,55,55,55)
      except lrkmaster.LRKError:
        lost += 1
      resendReg = int('0x'+lrk.readReg(8),16)
      plos = resendReg >> 4
      arc = resendReg & 0x0F
      resent += arc
      place += 1
    print 'packets sent: '+str(packets)+' - packets resent: '+str(resent)+'('+str((100*resent)/packets)+'%) - packets lost: '+str(lost)+'('+str((100*lost)/packets)+'%)'

