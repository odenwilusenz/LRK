/*
 * LRK.asm
 *
 *  Created: 22.12.2015 00:22:14
 *   Author: Lantti
 *
 *	Lichtröhrlikontroller
 */ 


/*
  Reg summary

  r0, all interrupt handlers (saves SREG)
  r1, 
  r2, 
  r3, 
  r4, 
  r5, 
  r6, 
  r7, 
  r8, 
  r9, 
  r10, 
  r11,
  r12, 
  r13, 
  r14, 
  r15, 
  r16, mainloop, spi_op, init
  r17,
  r18, mainloop
  r19, mainloop, spi_op
  r20, spi_op
  r21, spi_op
  r22, all interrupt handlers (work reg)
  r23,
  r24, 
  r25, 
  r26 (Xl), init
  r27 (Xh), init
  r28 (Yl), init
  r29 (Yh), init
  r30 (Zl), init, mainloop, spi_op
  r31 (Zh), init, mainloop, spi_op
*/


.INCLUDE "tn44Adef.inc"

.equ LEDB1 = PORTA0
.equ LEDB2 = PORTA1
.equ LEDG1 = PORTA2
.equ LEDG2 = PORTA3
.equ SCK = PORTA4
.equ MISO = PORTA5
.equ MOSI = PORTA6
.equ CSN = PORTA7

.equ IRQ = PORTB0
.equ LEDR1 = PORTB1
.equ LEDR2 = PORTB2
.equ CE = PORTB3

.equ IRQ_PCMSKREG = PCMSK1
.equ IRQ_PCIE = PCIE1
.equ IRQ_PCINT = PCINT8

.equ PORTA_DDR = (1<<LEDB1)+(1<<LEDB2)+(1<<LEDG1)+(1<<LEDG2)+(1<<SCK)+(0<<MISO)+(1<<MOSI)+(1<<CSN)
.equ PORTA_UP =  (0<<LEDB1)+(0<<LEDB2)+(0<<LEDG1)+(0<<LEDG2)+(0<<SCK)+(1<<MISO)+(0<<MOSI)+(1<<CSN)

.equ PORTB_DDR = (0<<IRQ)+(1<<LEDR1)+(1<<LEDR2)+(1<<CE)
.equ PORTB_UP =  (1<<IRQ)+(0<<LEDR1)+(0<<LEDR2)+(0<<CE)

.equ WD_TIMEOUT = 7
.equ WDP_BITS = (((WD_TIMEOUT & 8) << 2) | (WD_TIMEOUT & 7)) 

.equ R_REGISTER =            0b00000000
.equ W_REGISTER =            0b00100000
.equ R_RX_PAYLOAD =          0b01100001
.equ W_TX_PAYLOAD =          0b10100000
.equ FLUSH_TX =              0b11100001
.equ FLUSH_RX =              0b11100010
.equ REUSE_TX_PL =           0b11100011
.equ R_RX_PL_WID =           0b01100000
.equ W_ACK_PAYLOAD =         0b10101000
.equ W_TX_PAYLOAD_NO_ACK =   0b10110000
.equ RF_NOP =                0b11111111

.equ CONFIG =      0x00
.equ EN_AA =       0x01
.equ EN_RXADDR =   0x02
.equ SETUP_AW =    0x03
.equ SETUP_RETR =  0x04
.equ RF_CH =       0x05
.equ RF_SETUP =    0x06
.equ STATUS =      0x07
.equ OBSERVE_TX =  0x08
.equ RPD =         0x09
.equ RX_ADDR_P0 =  0x0A
.equ RX_ADDR_P1 =  0x0B
.equ RX_ADDR_P2 =  0x0C
.equ RX_ADDR_P3 =  0x0D
.equ RX_ADDR_P4 =  0x0E
.equ RX_ADDR_P5 =  0x0F
.equ TX_ADDR =     0x10
.equ RX_PW_P0 =    0x11
.equ RX_PW_P1 =    0x12
.equ RX_PW_P2 =    0x13
.equ RX_PW_P3 =    0x14
.equ RX_PW_P4 =    0x15
.equ RX_PW_P5 =    0x16
.equ FIFO_STATUS = 0x17
.equ DYNPD =       0x1C
.equ FEATURE =     0x1D




.DSEG
.ORG 0x60
                .BYTE 47
stack:		.BYTE 1
                .BYTE 1
bufferc:	.BYTE 32

.CSEG
                        ;Interrupt vectors
			rjmp   RESET_H          ; Reset Handler
			rjmp   INT0_H           ; IRQ0 Handler
			rjmp   PCINT0_H         ; PCINT0 Handler
			rjmp   PCINT1_H         ; PCINT1 Handler
			rjmp   WDT_H            ; Watchdog Interrupt Handler
			rjmp   TIM1_CAPT_H      ; Timer1 Capture Handler
			rjmp   TIM1_COMPA_H     ; Timer1 Compare A Handler
			rjmp   TIM1_COMPB_H     ; Timer1 Compare B Handler
			rjmp   TIM1_OVF_H       ; Timer1 Overflow Handler
			rjmp   TIM0_COMPA_H     ; Timer0 Compare A Handler
			rjmp   TIM0_COMPB_H     ; Timer0 Compare B Handler
			rjmp   TIM0_OVF_H       ; Timer0 Overflow Handler
			rjmp   ANA_COMP_H       ; Analog Comparator Handler
			rjmp   ADC_CONV_H       ; ADC Conversion Handler
			rjmp   EE_RDY_H         ; EEPROM Ready Handler
			rjmp   USI_STR_H        ; USI STart Handler
			rjmp   USI_OVF_H        ; USI Overflow Handler

                        ;RF recieve pipe widths
PW_TABLE:               .DB 32,1,1,1,1

                        ;RF receive pipe callback vectors
PIPE_CB_VECT:           rjmp   INIT
                        rjmp   PIPE1_CB
                        rjmp   PIPE2_CB
                        rjmp   PIPE3_CB
                        rjmp   PIPE4_CB
                        rjmp   PIPE5_CB

INT0_H:           ; IRQ0 Handler
PCINT0_H:         ; PCINT0 Handler
PCINT1_H:         ; PCINT1 Handler
WDT_H:            ; Watchdog Interrupt Handler
TIM1_CAPT_H:      ; Timer1 Capture Handler
TIM1_COMPA_H:     ; Timer1 Compare A Handler
TIM1_COMPB_H:     ; Timer1 Compare B Handler
TIM1_OVF_H:       ; Timer1 Overflow Handler
TIM0_COMPA_H:
TIM0_COMPB_H:
TIM0_OVF_H:
ANA_COMP_H:       ; Analog Comparator Handler
ADC_CONV_H:       ; ADC Conversion Handler
EE_RDY_H:         ; EEPROM Ready Handler
USI_STR_H:        ; USI STart Handler
USI_OVF_H:        ; USI Overflow Handler
			reti

PIPE1_CB:               sbi PORTA,LEDB1
                        sbi PORTA,LEDB2
                        cbi PORTA,LEDG1
                        cbi PORTA,LEDG2
                        cbi PORTB,LEDR1
                        cbi PORTB,LEDR2
                        ret
PIPE2_CB:               sbi PORTA,LEDB1
                        sbi PORTA,LEDB2
                        sbi PORTA,LEDG1
                        sbi PORTA,LEDG2
                        cbi PORTB,LEDR1
                        cbi PORTB,LEDR2
                        ret
PIPE3_CB:               cbi PORTA,LEDB1
                        cbi PORTA,LEDB2
                        sbi PORTA,LEDG1
                        sbi PORTA,LEDG2
                        sbi PORTB,LEDR1
                        sbi PORTB,LEDR2
                        ret
PIPE4_CB:               sbi PORTA,LEDB1
                        cbi PORTA,LEDB2
                        sbi PORTA,LEDG1
                        cbi PORTA,LEDG2
                        sbi PORTB,LEDR1
                        cbi PORTB,LEDR2
                        ret
PIPE5_CB:               cbi PORTA,LEDB1
                        sbi PORTA,LEDB2
                        cbi PORTA,LEDG1
                        sbi PORTA,LEDG2
                        cbi PORTB,LEDR1
                        sbi PORTB,LEDR2
                        ret


INIT:
                        ret



.ORG 0x600
/* After reset initialze stack, pointers (XYZ), IO, interrupts and timer0
   Mangels r16, r23 and pointers X, Y and Z
   
   Starts timer0 to drive the PWM routine*/
RESET_H:
			ldi r16, HIGH(stack)
			out SPH, r16
			ldi r16, LOW(stack)
			out SPL, r16

                        ldi r16, 0
                        out MCUSR, r16

                        ldi r16, (0<<WDIF|0<<WDIE|0<<WDP3|1<<WDCE|1<<WDE|0<<WDP2|0<<WDP1|0<<WDP0)
                        out WDTCSR, r16

                        ldi r16, (0<<WDIF|0<<WDIE|0<<WDCE|0<<WDE|WDP_BITS)
                        out WDTCSR, r16

			clr r31
			clr r29
			clr r27

			ldi r16, PORTA_UP
			out PORTA, r16
			ldi r16, PORTA_DDR
			out DDRA, r16

			ldi r16, PORTB_UP
			out PORTB, r16
			ldi r16, PORTB_DDR
			out DDRB, r16

			ldi r16, (1<<SE)
			out MCUCR, r16
			ldi r16, (1<<PRUSI)+(1<<PRADC)
			out PRR, r16

			ldi r16, (1<<IRQ_PCIE)
			out GIMSK, r16
			ldi r16, (1<<IRQ_PCINT)
			out IRQ_PCMSKREG, r16

			ldi r30, bufferc-1
			ldi r16, R_REGISTER + RX_ADDR_P0
			st Z,r16
			ldi r16,5
			rcall spi_op


                        sbi PORTB,LEDR1
                        sbi PORTB,LEDR2
                        sbi PORTA,LEDG1
                        sbi PORTA,LEDG2
			ldi r28, bufferc-1
			ld r16,Y+
			cpi r16,0b00001110
			brne funkfail
			ldi r23,5
funkcheckloop:		ld r16,Y+
			cpi r16,0xE7
			brne funkfail
			dec r23
			brne funkcheckloop
                        cbi PORTB,LEDR1
                        cbi PORTB,LEDR2
                        rjmp funkok
funkfail:		cbi PORTA,LEDG1
                        cbi PORTA,LEDG2
funkok:

			ldi r30,bufferc
                        ldi r16,0b00111111
                        st  Z,r16
			ldi r16,W_REGISTER + EN_RXADDR   ;enable all rf pipes
			st -Z,r16
			ldi r16,1
			rcall spi_op

			ldi r30,bufferc
                        ldi r16,1
                        st  Z,r16
			ldi r16,W_REGISTER + SETUP_AW   ;set rf address width to 3 bytes
			st -Z,r16
			ldi r16,1
			rcall spi_op


			ldi r16,2
eereadloop:		out EEARL,r16		;read rf-parameters stored on the eeprom
			sbi EECR,EERE
			in r23,EEDR
			push r23
			dec r16
			brpl eereadloop

                        ldi r30,bufferc
                        pop r16
                        st Z,r16
			ldi r16,W_REGISTER + RF_CH	;write channel number to rf
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        pop r18
                        pop r17
                        ldi r16,0xE7
                        ldi r30,bufferc+2
                        st  Z,r18
                        st  -Z,r17
                        st  -Z,r16
			ldi r16,W_REGISTER + RX_ADDR_P0	;write control pipe address to rf
			st -Z,r16
			ldi r16,3
			rcall spi_op

                        ldi r16,0xC2
                        ldi r30,bufferc+2
                        st  Z,r18
                        st  -Z,r17
                        st  -Z,r16
			ldi r16,W_REGISTER + RX_ADDR_P1	;write pipe1 address to rf
			st -Z,r16
			ldi r16,3
			rcall spi_op



                        ldi r30, bufferc
			ldi r16,32		        ;set control pipe length
			st Z,r16
			ldi r16, W_REGISTER + RX_PW_P0
			st -Z,r16
			ldi r16,1
			rcall spi_op

/*
                        ldi r30, bufferc
			ldi r16,32		        ;set control pipe length
			st Z,r16
			ldi r16, W_REGISTER + RX_PW_P1
			st -Z,r16
			ldi r16,1
			rcall spi_op
*/


                        ldi r30,PW_TABLE<<1
                        lpm r16,Z
                        ldi r30,bufferc
                        st Z,r16
			ldi r16,W_REGISTER + RX_PW_P1	;set pipe1 length
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        ldi r30,(PW_TABLE<<1)+1
                        lpm r16,Z
                        ldi r30,bufferc
                        st Z,r16
			ldi r16,W_REGISTER + RX_PW_P2	;set pipe2 length
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        ldi r30,(PW_TABLE<<1)+2
                        lpm r16,Z
                        ldi r30,bufferc
                        st Z,r16
			ldi r16,W_REGISTER + RX_PW_P3	;set pipe3 length
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        ldi r30,(PW_TABLE<<1)+3
                        lpm r16,Z
                        ldi r30,bufferc
                        st Z,r16
			ldi r16,W_REGISTER + RX_PW_P4	;set pipe4 length
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        ldi r30,(PW_TABLE<<1)+4
                        lpm r16,Z
                        ldi r30,bufferc
                        st Z,r16
			ldi r16,W_REGISTER + RX_PW_P5	;set pipe5 length
			st -Z,r16
			ldi r16,1
			rcall spi_op


			ldi r30, bufferc
			ldi r16, 0b00001011	;set rf-module to power-on and RX mode
			st Z,r16
			ldi r16, W_REGISTER + CONFIG
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        rcall PIPE_CB_VECT

			sei                   ; Enable interrupts

/*Main loop
  Waits for interrupt, checks if there is a new packet to read,
  if yes, reads the packet, sets new values to the PWM routine and
  returns to wait
  Mangels: Z,r16,r18,r19,r20,r21
*/
FOREVER:	        sleep
			sbic PINB,IRQ
			rjmp FOREVER

rf_op:                  ldi r16, RF_NOP  ;read status to get the current pipe number
                        ldi r30, bufferc
                        st  -Z,r16
                        clr r16
                        rcall spi_op   ;leaves the last byte read on r19, no need to ld from mem

                        andi r19, 0b00001110
                        breq control_command
                        cpi r19,0x0E
                        breq FOREVER
                        
                        lsr r19
                        mov r18,r19           ;pipe number of the current pipe
                        ldi r30,(PW_TABLE<<1)-1
                        add r30,r18
                        lpm r16,Z             ;get the width of the current pipe

                        ldi r30, bufferc
			ldi r19,R_RX_PAYLOAD  ;read packet
			st  -Z,r19
			rcall spi_op

                        ldi r30,PIPE_CB_VECT
                        add r30,r18
                        icall

clear_irq:              ldi r30, bufferc
			ldi r16, 0b01110000	;IRQs to clear
			st Z,r16
			ldi r16, W_REGISTER + STATUS
			st -Z,r16
			ldi r16,1
			rcall spi_op

                        rjmp rf_op

control_command:           
                        ldi r30, bufferc-1
			ldi r16,R_RX_PAYLOAD  ;read packet
			st  Z,r16
			ldi r16,32              ;pipe width
                        rcall spi_op

                        cbi PORTA,LEDG1
                        cbi PORTA,LEDG2
                        cbi PORTA,LEDB1
                        cbi PORTA,LEDB2
                        cbi PORTB,LEDR1
                        cbi PORTB,LEDR2
                        sbrs r19,0
                        sbi PORTB,LEDR2

                        rjmp clear_irq





/*SPI operations subroutine
  Requires a pointer to the SPI transfer buffer in pointer Z and
  transfer length - 1 in r16
  Returns: SPI operation response in the transfer buffer
  Mangles: Z, r16, r19, r20, r21*/
spi_op:
			cbi PORTA,CSN
spi_byte:		ldi r20,7
			ld r19,Z
spi_bit:		in r21,PINA
			andi r21,(1<<MISO)
			neg r21
			rol r19
			brcs spi_set
			cbi PORTA,MOSI
			rjmp spi_clear
spi_set:		sbi PORTA,MOSI
			nop
			nop
spi_clear:		sbi PORTA,SCK
			nop
			nop
			cbi PORTA,SCK
			dec r20
			brpl spi_bit
			st Z+,r19
			dec r16
			brpl spi_byte
spi_done:		sbi PORTA,CSN
			ret
