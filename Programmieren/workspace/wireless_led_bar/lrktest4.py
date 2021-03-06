import rpyc
import plumbum
import sys
import time

addressMap = [1,3,5,7,9,11,15,17,19,21,23,25]

with plumbum.SshMachine(sys.argv[1], sys.argv[2]) as sshmachine, rpyc.ssh_connect(sshmachine, int(sys.argv[3])) as conn:
  lrk = conn.root
  lrk.setRetry(0,0)
  packets = 0
  resent = 0
  lost = 0
  row = int(sys.argv[4]) % 256
  place = 0
  while True:
    place = 0
    resent = 0
    lost = 0
    starttime = time.time()
    for _ in range(12):
      if (not(lrk.do(row, addressMap[place],55,55,55,55,55,55))):
      if (not(True)):
        lost += 1
      resent += lrk.readReg(8,1)[0]&0x0F
      place += 1
    stoptime = time.time()
    print ('sent: 12 - resent: '+str(resent)+'('+str((100*resent)/12)+'%) - lost: '+str(lost)+'('+str((100*lost)/12)+'%) - time: '+str(stoptime-starttime)+'s')

