import lrkmaster
import sys

with lrkmaster.LRKmaster(sys.argv[1]) as lrk:
  while True:
    row = int(raw_input('ROW ')) 
    place = int(raw_input('PLACE ')) 
    r1 = int(raw_input('R1 '))
    g1 = int(raw_input('G1 '))
    b1 = int(raw_input('B1 '))
    r2 = int(raw_input('R2 '))
    g2 = int(raw_input('G2 '))
    b2 = int(raw_input('B2 '))
    lrk.do(row, place, r1,g1,b1,r2,g2,b2)
