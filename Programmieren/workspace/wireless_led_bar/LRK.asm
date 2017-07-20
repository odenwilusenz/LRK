/*
 * LRK.asm
 *
 *  Created: 22.12.2015 00:22:14
 *   Author: Lantti
 *
 *	Lichtröhrlikontroller
 */ 



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

.equ PRESCALER_MODE = 3

.equ PWMCHA = 4
.equ PWMCHB = 2
.equ PWMMSKA = (1<<LEDB1)+(1<<LEDB2)+(1<<LEDG1)+(1<<LEDG2)
.equ PWMMSKB = (1<<LEDR1)+(1<<LEDR2)
.equ DATAPLEN = 2*PWMCHA+2*PWMCHB+2		;must be at least 8
.equ CTRLPLEN = 32

.equ R_RX_PAYLOAD = 0b01100001
.equ R_REGISTER_STATUS = 0b00000111
.equ R_REGISTER_RX_ADDR_P0 = 0b00001010
.equ W_REGISTER_CONFIG = 0b00100000
.equ W_REGISTER_STATUS = 0b00100111
.equ W_REGISTER_RX_PW_P0 = 0b00110001
.equ W_REGISTER_RX_ADDR_P0 = 0b00101010
.equ W_REGISTER_RX_PW_P1 = 0b00110010
.equ W_REGISTER_RX_ADDR_P1 = 0b00101011
.equ W_REGISTER_RF_CH = 0b00100101
.equ FLUSH_RX = 0b11100010


.DSEG
		.BYTE 1
bufferc:	.BYTE CTRLPLEN
.ORG 0x60	;the addresses of the buffers are highly magical and need to be left as is and the previous byte kept free too
		.BYTE 1
buffer0:	.BYTE DATAPLEN
.ORG 0x9E	;the addresses of the buffers are highly magical and need to be left as is and the previous byte kept free too
		.BYTE 1
buffer1:	.BYTE DATAPLEN
		.BYTE 128
stack:		.BYTE 1

.CSEG
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


defaultgreen:		.DB 128,(1<<LEDG2),0,0,0,0,0,0,0,0,0,0,0,0
defaultred:		.DB 0,0,0,0,0,0,0,0,0,0,(1<<LEDR2),0,0,0

INT0_H:           ; IRQ0 Handler
PCINT0_H:         ; PCINT0 Handler
PCINT1_H:         ; PCINT1 Handler
WDT_H:            ; Watchdog Interrupt Handler
TIM1_CAPT_H:      ; Timer1 Capture Handler
TIM1_COMPA_H:     ; Timer1 Compare A Handler
TIM1_COMPB_H:     ; Timer1 Compare B Handler
TIM1_OVF_H:       ; Timer1 Overflow Handler
ANA_COMP_H:       ; Analog Comparator Handler
ADC_CONV_H:       ; ADC Conversion Handler
EE_RDY_H:         ; EEPROM Ready Handler
USI_STR_H:        ; USI STart Handler
USI_OVF_H:        ; USI Overflow Handler
			reti


/* After reset initialze stack, pointers (XYZ), IO, interrupts and timer0
   Mangels r16, r23 and pointers X and Y
   
   Starts timer0 to drive the PWM routine*/
RESET_H:
			ldi r16, HIGH(stack)
			out SPH, r16
			ldi r16, LOW(stack)
			out SPL, r16

			clr r31
			clr r29
			clr r27

			ldi r16, (1<<MISO)+(1<<CSN)
			out PORTA, r16
			ldi r16, (1<<LEDB1)+(1<<LEDB2)+(1<<LEDG1)+(1<<LEDG2)+(1<<SCK)+(1<<MOSI)+(1<<CSN)
			out DDRA, r16

			ldi r16, (1<<IRQ)
			out PORTB, r16
			ldi r16, (1<<LEDR1)+(1<<LEDR2)+(1<<CE)
			out DDRB, r16

			ldi r16, (1<<SE)
			out MCUCR, r16
			ldi r16, (1<<PRUSI)+(1<<PRADC)
			out PRR, r16

			ldi r16, (1<<PCIE1)
			out GIMSK, r16
			ldi r16, (1<<PCINT8)
			out PCMSK1, r16

			ldi r16, (1<<TOIE0)+(1<<OCIE0A)+(1<<OCIE0B)
			out TIMSK0, r16		;enable the PWM interrupts
			ldi r16, PRESCALER_MODE
			out TCCR0B, r16		;start the timer and PWM routine


			ldi r26, buffer0-1
			ldi r16, R_REGISTER_RX_ADDR_P0
			st X,r16
			ldi r16,5
			rcall spi_op

			ldi r30,(defaultgreen<<1)
			ldi r28, buffer0-1
			ld r16,Y+
			cpi r16,0b00001110
			brne funkfail
			ldi r23,3
funkcheckloop:		ld r16,Y+
			cpi r16,0xE7
			brne funkfail
			dec r23
			brpl funkcheckloop
			ld r16,Y
			cpi r16,0xE7
			breq funkok
funkfail:		ldi r30,(defaultred<<1)
funkok:			
			ldi r28,buffer1
			ldi r16,DATAPLEN-1
defcol_loop:		lpm r23,Z+
			st Y+,r23
			dec r16
			brpl defcol_loop


			ldi r16,10
			ldi r26,bufferc+12
eereadloop:		out EEARH,r31
			out EEARL,r16		;read rf-parameters stored on the eeprom
			sbi EECR,EERE
			in r23,EEDR
			st -X,r23
			dec r16
			brpl eereadloop

			ldi r16,W_REGISTER_RX_ADDR_P0	;write data pipe address to rf
			st -X,r16
			ldi r16,5
			rcall spi_op

			ldi r26, bufferc+5
			ldi r16,W_REGISTER_RX_ADDR_P1	;write control pipe address to rf
			st X,r16
			ldi r16,5
			rcall spi_op

			ldi r26, bufferc+10
			ldi r16,W_REGISTER_RF_CH	;write channel number to rf
			st X,r16
			ldi r16,1
			rcall spi_op

			ldi r26, bufferc
			ldi r16,DATAPLEN		;set data pipe length
			st X,r16
			ldi r16, W_REGISTER_RX_PW_P0
			st -X,r16
			ldi r16,1
			rcall spi_op

			ldi r26, bufferc
			ldi r16,CTRLPLEN		;set control pipe length
			st X,r16
			ldi r16, W_REGISTER_RX_PW_P1
			st -X,r16
			ldi r16,1
			rcall spi_op


			ldi r26, bufferc
			ldi r16, 0b00001011	;set rf-module to power-on and RX mode
			st X,r16
			ldi r16, W_REGISTER_CONFIG
			st -X,r16
			ldi r16,1
			rcall spi_op

			ldi r23, buffer1     ; set initial pwm list pointer

			sei                   ; Enable interrupts

/*Main loop
  Waits for interrupt, checks if there is a new packet to read,
  if yes, reads the packet, sets new values to the PWM routine and
  returns to wait
  Mangels: X,Y,r16,r17
           (Mangling Y and r17 happen only while timer0 is reset and stopped
		    when I belive it is safe)*/
FOREVER:	
			sleep
			sbic PINB,IRQ
			rjmp FOREVER

			mov r26,r23
			neg r26
			dec r26
			ldi r16,R_RX_PAYLOAD  ;read packet
			st X,r16
			ldi r16,DATAPLEN
			rcall spi_op

			mov r26,r23
			neg r23			;point the PWM routines to the new pwmlist

			ldi r16, 0b01110000	;clear IRQ
			st X,r16
			ldi r16, W_REGISTER_STATUS
			st -X,r16
			ldi r16,1
			rcall spi_op

			ldi r16, FLUSH_RX
			st -X,r16
			ldi r16,0
			rcall spi_op

			rjmp FOREVER

/*Timer0 Compare A Handler
  Toggles the PWM A outputs given by the mask in r17
  Sets the next event time and output mask if needed
  Requires: A bitmask of the PWM A outputs to toggle in r17
            A pointer to the current position of PWM A list in Y
  Returns: A new bitmask of the PWM A outputs to toggle next in r17
           A new pointer to the new position of PWM A list in Y
  Mangels: r0, r22
*/
TIM0_COMPA_H:
			in r0, SREG
			ld r22, Y+
			andi r22,PWMMSKA
			out PINA, r22
			ld r22, Y+
			out OCR0A, r22
			out SREG,r0
			reti
/*Timer0 Compare B Handler
  Toggles the PWM B outputs given by the mask in r18
  Sets the next event time and output mask if needed
  Requires: A bitmask of the PWM B outputs to toggle in r18
            A pointer to the current position of PWM B list in Z
  Returns: A new bitmask of the PWM B outputs to toggle next in r18
           A new pointer to the new position of PWM B list in Z
  Mangels: r0, r22
*/
TIM0_COMPB_H:
			in r0, SREG
			ld r22, Z+
			andi r22, PWMMSKB
			out PINB, r22
			ld r22, Z+
			out OCR0B, r22
			out SREG,r0
			reti

/* Timer0 Overflow Handler
   Sets PWM outputs HIGH
   Sets pointer Y to the beginning of the next PWM list A
   Sets pointer Z to the beginning of the next PWM list B
   Sets the first PWM event times and first output masks
   Requires: Pointer to the next pair of PWM lists in r23
   Returns: PWM list A in Y,
            PWM list B in Z,
   Mangles: r0, r22*/
TIM0_OVF_H:
			in r0, SREG
			cbi PORTA, LEDB1
			cbi PORTA, LEDB2
			cbi PORTA, LEDG1
			cbi PORTA, LEDG2
			cbi PORTB, LEDR1
			cbi PORTB, LEDR2
			mov r28, r23
			mov r30, r23
			subi r30,-(2*PWMCHA+1)
			ld r22, Y+
			out OCR0A, r22
			ld r22, Z+
			out OCR0B, r22
			out SREG,r0
			reti

/*SPI operations subroutine
  Requires a pointer to the SPI transfer buffer in pointer X and
  transfer length - 1 in r16
  Returns: SPI operation response in the transfer buffer
  Mangles: X, r16, r19, r20, r21*/
spi_op:
			cbi PORTA,CSN
spi_byte:		ldi r20,7
			ld r19,X
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
			st X+,r19
			dec r16
			brpl spi_byte
spi_done:		sbi PORTA,CSN
			ret
