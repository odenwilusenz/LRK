EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:LKR
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ATTINY24A-SS IC1
U 1 1 56697127
P 2450 4000
F 0 "IC1" H 1600 4750 50  0000 C CNN
F 1 "ATTINY24A-SS" H 3100 3250 50  0000 C CNN
F 2 "LRK:SOIC-14_hand" H 2450 3800 50  0000 C CIN
F 3 "" H 2450 4000 50  0000 C CNN
	1    2450 4000
	1    0    0    -1  
$EndComp
$Comp
L RFMODULE P2
U 1 1 56698FB3
P 5050 4050
F 0 "P2" H 5050 4300 50  0000 C CNN
F 1 "RFMODULE" H 5150 3800 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04" H 5050 2850 50  0001 C CNN
F 3 "" H 5050 2850 50  0000 C CNN
	1    5050 4050
	1    0    0    -1  
$EndComp
$Comp
L LEDS P4
U 1 1 56699056
P 9750 3100
F 0 "P4" H 9750 3350 50  0000 C CNN
F 1 "LEDS" V 9950 3100 50  0000 C CNN
F 2 "LRK:Pin_Header_Straight_1x04" H 9750 3100 50  0001 C CNN
F 3 "" H 9750 3100 50  0000 C CNN
	1    9750 3100
	0    -1   -1   0   
$EndComp
$Comp
L LEDS P3
U 1 1 56699111
P 7050 3100
F 0 "P3" H 7050 3350 50  0000 C CNN
F 1 "LEDS" V 7250 3100 50  0000 C CNN
F 2 "LRK:Pin_Header_Straight_1x04" H 7050 3100 50  0001 C CNN
F 3 "" H 7050 3100 50  0000 C CNN
	1    7050 3100
	0    -1   -1   0   
$EndComp
$Comp
L PWR P1
U 1 1 56699A47
P 1700 1150
F 0 "P1" H 1700 1300 50  0000 C CNN
F 1 "PWR" V 1900 1150 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 1700 1150 50  0001 C CNN
F 3 "" H 1700 1150 50  0000 C CNN
	1    1700 1150
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR01
U 1 1 5669A4A0
P 3200 1500
F 0 "#PWR01" H 3200 1250 50  0001 C CNN
F 1 "GND" H 3200 1350 50  0000 C CNN
F 2 "" H 3200 1500 50  0000 C CNN
F 3 "" H 3200 1500 50  0000 C CNN
	1    3200 1500
	1    0    0    -1  
$EndComp
$Comp
L +12V #PWR02
U 1 1 5669A591
P 2650 1000
F 0 "#PWR02" H 2650 850 50  0001 C CNN
F 1 "+12V" H 2650 1140 50  0000 C CNN
F 2 "" H 2650 1000 50  0000 C CNN
F 3 "" H 2650 1000 50  0000 C CNN
	1    2650 1000
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR03
U 1 1 5669A5B6
P 3750 1000
F 0 "#PWR03" H 3750 850 50  0001 C CNN
F 1 "+3.3V" H 3750 1140 50  0000 C CNN
F 2 "" H 3750 1000 50  0000 C CNN
F 3 "" H 3750 1000 50  0000 C CNN
	1    3750 1000
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR04
U 1 1 5669AA03
P 1300 2900
F 0 "#PWR04" H 1300 2750 50  0001 C CNN
F 1 "+3.3V" H 1300 3040 50  0000 C CNN
F 2 "" H 1300 2900 50  0000 C CNN
F 3 "" H 1300 2900 50  0000 C CNN
	1    1300 2900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR05
U 1 1 5669AA32
P 1300 5450
F 0 "#PWR05" H 1300 5200 50  0001 C CNN
F 1 "GND" H 1300 5300 50  0000 C CNN
F 2 "" H 1300 5450 50  0000 C CNN
F 3 "" H 1300 5450 50  0000 C CNN
	1    1300 5450
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 5669B3C8
P 3750 1250
F 0 "C2" H 3775 1350 50  0000 L CNN
F 1 "C" H 3775 1150 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3788 1100 50  0001 C CNN
F 3 "" H 3750 1250 50  0000 C CNN
	1    3750 1250
	1    0    0    -1  
$EndComp
$Comp
L +12V #PWR06
U 1 1 5669E30C
P 7500 2900
F 0 "#PWR06" H 7500 2750 50  0001 C CNN
F 1 "+12V" H 7500 3040 50  0000 C CNN
F 2 "" H 7500 2900 50  0000 C CNN
F 3 "" H 7500 2900 50  0000 C CNN
	1    7500 2900
	1    0    0    -1  
$EndComp
$Comp
L +12V #PWR07
U 1 1 5669E34A
P 10200 2900
F 0 "#PWR07" H 10200 2750 50  0001 C CNN
F 1 "+12V" H 10200 3040 50  0000 C CNN
F 2 "" H 10200 2900 50  0000 C CNN
F 3 "" H 10200 2900 50  0000 C CNN
	1    10200 2900
	1    0    0    -1  
$EndComp
Text Label 3550 3400 0    60   ~ 0
ledR1
Text Label 3550 4400 0    60   ~ 0
ledG1
Text Label 3550 3600 0    60   ~ 0
ledB1
Text Label 3550 4100 0    60   ~ 0
CSN
Text Label 3550 3800 0    60   ~ 0
SCK|SDO
Text Label 3550 3900 0    60   ~ 0
MISO|SII
Text Label 3550 4000 0    60   ~ 0
MOSI|SDI
Text Label 3550 4600 0    60   ~ 0
CE|RESET
Text Label 3550 3500 0    60   ~ 0
ledR2
Text Label 3550 4500 0    60   ~ 0
ledG2
Text Label 3550 3700 0    60   ~ 0
ledB2
Text Label 6250 4000 0    60   ~ 0
ledR1_out
Text Label 7050 4000 0    60   ~ 0
ledG1_out
Text Label 7350 3900 0    60   ~ 0
ledB1_out
Text Label 9000 4000 0    60   ~ 0
ledR2_out
Text Label 9750 4000 0    60   ~ 0
ledG2_out
Text Label 9950 3900 0    60   ~ 0
ledB2_out
Text Label 3550 4300 0    60   ~ 0
IRQ|SCI
$Comp
L IRLML2402 Q7
U 1 1 566A1AD9
P 10600 4300
F 0 "Q7" H 10900 4350 50  0000 R CNN
F 1 "IRLML2402" H 11150 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 10800 4400 50  0001 C CNN
F 3 "" H 10600 4300 50  0000 C CNN
	1    10600 4300
	1    0    0    -1  
$EndComp
$Comp
L IRLML2402 Q6
U 1 1 566A1B80
P 9700 4300
F 0 "Q6" H 10000 4350 50  0000 R CNN
F 1 "IRLML2402" H 10250 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 9900 4400 50  0001 C CNN
F 3 "" H 9700 4300 50  0000 C CNN
	1    9700 4300
	1    0    0    -1  
$EndComp
$Comp
L IRLML2402 Q5
U 1 1 566A1BD5
P 8800 4300
F 0 "Q5" H 9100 4350 50  0000 R CNN
F 1 "IRLML2402" H 9350 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 9000 4400 50  0001 C CNN
F 3 "" H 8800 4300 50  0000 C CNN
	1    8800 4300
	1    0    0    -1  
$EndComp
$Comp
L IRLML2402 Q4
U 1 1 566A1C2F
P 7900 4300
F 0 "Q4" H 8200 4350 50  0000 R CNN
F 1 "IRLML2402" H 8450 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 8100 4400 50  0001 C CNN
F 3 "" H 7900 4300 50  0000 C CNN
	1    7900 4300
	1    0    0    -1  
$EndComp
$Comp
L IRLML2402 Q3
U 1 1 566A1C90
P 7000 4300
F 0 "Q3" H 7300 4350 50  0000 R CNN
F 1 "IRLML2402" H 7550 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 7200 4400 50  0001 C CNN
F 3 "" H 7000 4300 50  0000 C CNN
	1    7000 4300
	1    0    0    -1  
$EndComp
$Comp
L IRLML2402 Q2
U 1 1 566A1CF8
P 6100 4300
F 0 "Q2" H 6400 4350 50  0000 R CNN
F 1 "IRLML2402" H 6650 4200 50  0000 R CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 6300 4400 50  0001 C CNN
F 3 "" H 6100 4300 50  0000 C CNN
	1    6100 4300
	1    0    0    -1  
$EndComp
$Comp
L AP2210 U1
U 1 1 566AB38B
P 3200 1100
F 0 "U1" H 3300 850 50  0000 C CNN
F 1 "3.3v reg" H 3200 1350 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-23_Handsoldering" H 3200 1100 50  0001 C CNN
F 3 "" H 3200 1100 50  0000 C CNN
	1    3200 1100
	1    0    0    -1  
$EndComp
$Comp
L C C3
U 1 1 566AB534
P 2650 1250
F 0 "C3" H 2675 1350 50  0000 L CNN
F 1 "C" H 2675 1150 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2688 1100 50  0001 C CNN
F 3 "" H 2650 1250 50  0000 C CNN
	1    2650 1250
	1    0    0    -1  
$EndComp
$Comp
L C C4
U 1 1 566AE2B3
P 5150 3500
F 0 "C4" H 5175 3600 50  0000 L CNN
F 1 "C" H 5175 3400 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 5188 3350 50  0001 C CNN
F 3 "" H 5150 3500 50  0000 C CNN
	1    5150 3500
	0    -1   -1   0   
$EndComp
$Comp
L R R3
U 1 1 566EA3FD
P 6000 4700
F 0 "R3" V 6080 4700 50  0000 C CNN
F 1 "R" V 6000 4700 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5930 4700 50  0001 C CNN
F 3 "" H 6000 4700 50  0000 C CNN
	1    6000 4700
	0    -1   -1   0   
$EndComp
$Comp
L R R4
U 1 1 566EA55B
P 6900 4800
F 0 "R4" V 6980 4800 50  0000 C CNN
F 1 "R" V 6900 4800 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 6830 4800 50  0001 C CNN
F 3 "" H 6900 4800 50  0000 C CNN
	1    6900 4800
	0    -1   -1   0   
$EndComp
$Comp
L R R5
U 1 1 566EA65A
P 7800 4900
F 0 "R5" V 7880 4900 50  0000 C CNN
F 1 "R" V 7800 4900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7730 4900 50  0001 C CNN
F 3 "" H 7800 4900 50  0000 C CNN
	1    7800 4900
	0    -1   -1   0   
$EndComp
$Comp
L R R7
U 1 1 566EA6C6
P 9600 5100
F 0 "R7" V 9680 5100 50  0000 C CNN
F 1 "R" V 9600 5100 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 9530 5100 50  0001 C CNN
F 3 "" H 9600 5100 50  0000 C CNN
	1    9600 5100
	0    -1   -1   0   
$EndComp
$Comp
L R R6
U 1 1 566EA75B
P 8700 5000
F 0 "R6" V 8780 5000 50  0000 C CNN
F 1 "R" V 8700 5000 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 8630 5000 50  0001 C CNN
F 3 "" H 8700 5000 50  0000 C CNN
	1    8700 5000
	0    -1   -1   0   
$EndComp
$Comp
L R R8
U 1 1 566EA7D3
P 10500 5200
F 0 "R8" V 10580 5200 50  0000 C CNN
F 1 "R" V 10500 5200 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 10430 5200 50  0001 C CNN
F 3 "" H 10500 5200 50  0000 C CNN
	1    10500 5200
	0    -1   -1   0   
$EndComp
$Comp
L PMEG2020EJ D1
U 1 1 566ED81C
P 2350 1400
F 0 "D1" H 2350 1500 50  0000 C CNN
F 1 "PMEG2020EJ" H 2350 1300 50  0000 C CNN
F 2 "LRK:SOD-323_hand" H 2350 1400 50  0001 C CNN
F 3 "" H 2350 1400 50  0000 C CNN
	1    2350 1400
	1    0    0    -1  
$EndComp
Text Label 2100 1200 0    60   ~ 0
0V
Wire Wire Line
	2650 1000 2650 1100
Wire Wire Line
	1900 1100 2900 1100
Wire Wire Line
	3200 1400 3200 1500
Wire Wire Line
	3500 1100 3750 1100
Wire Wire Line
	3750 1100 3750 1000
Wire Wire Line
	1300 2900 1300 3400
Wire Wire Line
	1300 3400 1400 3400
Wire Wire Line
	1300 4600 1300 5450
Wire Wire Line
	1300 4600 1400 4600
Wire Wire Line
	5700 3100 5700 3900
Wire Wire Line
	1300 3100 5700 3100
Connection ~ 1300 3100
Connection ~ 1300 5300
Wire Wire Line
	3500 3900 4400 3900
Wire Wire Line
	4700 3900 4800 3900
Wire Wire Line
	4400 3900 4400 4200
Wire Wire Line
	4400 4200 4800 4200
Wire Wire Line
	3500 4000 4300 4000
Wire Wire Line
	4300 4000 4300 4400
Wire Wire Line
	5700 4100 5500 4100
Wire Wire Line
	5700 3900 5500 3900
Wire Wire Line
	3500 3800 4500 3800
Wire Wire Line
	4500 3800 4500 4100
Wire Wire Line
	4500 4100 4800 4100
Wire Wire Line
	3500 3400 4100 3400
Wire Wire Line
	4100 3400 4100 4700
Wire Wire Line
	4100 4700 5850 4700
Wire Wire Line
	4000 4800 6750 4800
Wire Wire Line
	3500 3600 3900 3600
Wire Wire Line
	3900 3600 3900 4900
Wire Wire Line
	3900 4900 7650 4900
Wire Wire Line
	3800 5000 8550 5000
Wire Wire Line
	3700 5100 9450 5100
Wire Wire Line
	3600 3700 3600 5200
Wire Wire Line
	3600 5200 10350 5200
Connection ~ 4700 5300
Wire Wire Line
	5800 4700 5800 4300
Wire Wire Line
	5800 4300 5900 4300
Wire Wire Line
	10700 5300 1300 5300
Wire Wire Line
	6800 4300 6700 4300
Wire Wire Line
	6700 4300 6700 4800
Wire Wire Line
	7700 4300 7600 4300
Wire Wire Line
	7600 4300 7600 4900
Wire Wire Line
	6200 4500 6200 5300
Connection ~ 6200 5300
Wire Wire Line
	7100 4500 7100 5300
Connection ~ 7100 5300
Wire Wire Line
	8000 4500 8000 5300
Connection ~ 8000 5300
Wire Wire Line
	10700 4500 10700 5300
Wire Wire Line
	9800 4500 9800 5300
Connection ~ 9800 5300
Wire Wire Line
	8900 4500 8900 5300
Connection ~ 8900 5300
Wire Wire Line
	8500 5000 8500 4300
Wire Wire Line
	8500 4300 8600 4300
Wire Wire Line
	9400 5100 9400 4300
Wire Wire Line
	9400 4300 9500 4300
Wire Wire Line
	10300 5200 10300 4300
Wire Wire Line
	10300 4300 10400 4300
Wire Wire Line
	6200 4100 6200 4000
Wire Wire Line
	6200 4000 6900 4000
Wire Wire Line
	6900 4000 6900 3300
Wire Wire Line
	7100 4100 7100 4000
Wire Wire Line
	7100 4000 7000 4000
Wire Wire Line
	7000 4000 7000 3300
Wire Wire Line
	8000 4100 8000 3900
Wire Wire Line
	8000 3900 7100 3900
Wire Wire Line
	7100 3900 7100 3300
Wire Wire Line
	8900 4100 8900 4000
Wire Wire Line
	8900 4000 9600 4000
Wire Wire Line
	9600 4000 9600 3300
Wire Wire Line
	9800 4100 9800 4000
Wire Wire Line
	9800 4000 9700 4000
Wire Wire Line
	9700 4000 9700 3300
Wire Wire Line
	10700 4100 10700 3900
Wire Wire Line
	10700 3900 9800 3900
Wire Wire Line
	9800 3900 9800 3300
Wire Wire Line
	7200 3300 7200 3500
Wire Wire Line
	7200 3500 7500 3500
Wire Wire Line
	7500 3500 7500 2900
Wire Wire Line
	9900 3300 9900 3500
Wire Wire Line
	9900 3500 10200 3500
Wire Wire Line
	10200 3500 10200 2900
Wire Wire Line
	2500 1400 3750 1400
Connection ~ 3200 1400
Wire Wire Line
	4700 3900 4700 5300
Wire Wire Line
	4800 3900 4800 3500
Wire Wire Line
	4800 3500 5000 3500
Wire Wire Line
	5300 3500 5500 3500
Wire Wire Line
	5500 3500 5500 3900
Wire Wire Line
	4300 4400 5700 4400
Wire Wire Line
	5700 4400 5700 4100
Wire Wire Line
	3500 4600 4600 4600
Wire Wire Line
	4600 4600 4600 4000
Wire Wire Line
	4600 4000 4800 4000
Wire Wire Line
	3500 4300 4200 4300
Wire Wire Line
	4200 4300 4200 4500
Wire Wire Line
	4200 4500 5600 4500
Wire Wire Line
	5600 4500 5600 4200
Wire Wire Line
	5600 4200 5500 4200
Connection ~ 5800 4700
Wire Wire Line
	6150 4700 6200 4700
Connection ~ 6200 4700
Connection ~ 6700 4800
Wire Wire Line
	7050 4800 7100 4800
Connection ~ 7100 4800
Connection ~ 7600 4900
Wire Wire Line
	7950 4900 8000 4900
Connection ~ 8000 4900
Connection ~ 8500 5000
Wire Wire Line
	8850 5000 8900 5000
Connection ~ 8900 5000
Connection ~ 9400 5100
Wire Wire Line
	9750 5100 9800 5100
Connection ~ 9800 5100
Connection ~ 10300 5200
Wire Wire Line
	10650 5200 10700 5200
Connection ~ 10700 5200
Connection ~ 2650 1100
Wire Wire Line
	1900 1200 2100 1200
Wire Wire Line
	2100 1200 2100 1400
Wire Wire Line
	2100 1400 2200 1400
Connection ~ 2650 1400
Wire Wire Line
	3500 4100 4200 4100
Wire Wire Line
	4200 4100 4200 3700
Wire Wire Line
	4200 3700 5600 3700
Wire Wire Line
	5600 3700 5600 4000
Wire Wire Line
	5600 4000 5500 4000
Wire Wire Line
	3600 3700 3500 3700
Wire Wire Line
	4000 4400 4000 4800
Wire Wire Line
	3800 5000 3800 3500
Wire Wire Line
	3800 3500 3500 3500
Wire Wire Line
	4000 4400 3500 4400
Wire Wire Line
	3700 5100 3700 4500
Wire Wire Line
	3700 4500 3500 4500
$EndSCHEMATC
