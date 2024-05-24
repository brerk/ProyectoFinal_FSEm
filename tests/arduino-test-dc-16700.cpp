/*
* arduino-test-dc.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Controls the power output of a resistive load using
* zero-cross detection and a TRIAC. Code for Arduino UNO
*
*/

// TRIAC BT137

#include <sys/time.h>


#define ZXPIN 2 // Digital 2 is Pin 2 in UNO - Cruce por zero
#define TRIAC 3 // Digital 3 is Pin 3 in UNO - control TRIAC which controls AC

// Globals
volatile bool flag = false; // Indica si hay cruce por cero
int pdelay = 8035;				// Delay before turning on the TRIAC

long start_zero = 0
	
long microseconds_zero = 0;



// Prototypes
void turnLampOn(void);
long getMicrotime();

long getMicrotime(){
	struct timeval currentTime;
	gettimeofday(&currentTime, NULL);
	return currentTime.tv_sec * (int)1e6 + currentTime.tv_usec;
}

/**
* Setup the Arduino
*/
void setup(void){
	// Setup interupt pin (input)
	pinMode(ZXPIN, INPUT);

	// digitalPinToInterrupt may not work, so we choose directly the
	// interrupt number. It is Zero for pin 2 on Arduino UNO
	// attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
	attachInterrupt(0, zxhandle, RISING);

	// Setup output (triac) pin
	pinMode(TRIAC, OUTPUT);

	// Blink led on interrupt
	pinMode(13, OUTPUT);

	Serial.begin(9600); // Serial comunication
}

void loop(){
	// Check if buffer has data and reads an int from console, which is used as pdelay
	while (Serial.available() > 0){
		// pdelay = Serial.parseInt();
		Serial.println("Wtf is this?");
	}
}

void turnLampOn(){
	/*
	 *	Turn on Lamp
	*/

	// Turn sentinel LED on
	digitalWrite(13, HIGH);

	// Send a 20us pulse to the TRIAC
	digitalWrite(TRIAC, HIGH);

	delayMicroseconds(300);

	digitalWrite(TRIAC, LOW);
}

void zxhandle(){
	/*
	 * Executed when an interruption is received, meaning zero is crossed
	*/

	flag = true;

	if start_zero == 0 {
		start_zero = getMicrotime()
	} else {
		microseconds_zero =  getMicrotime() - start_zero;
	}



	// TRIAC automatically shuts down on ZX
	digitalWrite(TRIAC, LOW);	// TRIAC
	digitalWrite(13, LOW);		// STATUS LED

	delayMicroseconds(pdelay);

	if(pdelay > 0) turnLampOn();
}
