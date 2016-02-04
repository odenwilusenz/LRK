import lrkmaster
import sys
import random
import time

with lrkmaster.LRKmaster(sys.argv[1]) as lrk:
  row = int(sys.argv[2]) % 256
  place = int(sys.argv[3]) % 256
  c = [0,0,0,0,0,0] 
  cc = [0,0,0,0,0,0]
  while True:
    cc = map(lambda x: random.randint(-1,1), cc)
    for _ in range(64):
      lrk.do(row, place, abs(c[0])%256,abs(c[1])%256,abs(c[2])%256,abs(c[3])%256,abs(c[4])%256,abs(c[5])%256)
      for i in range(6):
        c[i] = c[i]+random.randint(-1,1)+cc[i]
        if (c[i] > 255):
          c[i] = 255
        if (c[i] < -255):
          c[i] = -255
        time.sleep(0.005)
