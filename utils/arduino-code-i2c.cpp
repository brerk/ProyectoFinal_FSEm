// Arduino I2C handler: Control a light power, fan power, water pump state on/off and 2 analogic sensors.
// Copyright (C) 2024  Ivan Martinez,Erik Bravo
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
#include <Wire.h>

#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13
#define VAREF 2.7273

float lightPower = 0;
float fanPower = 0;
float pumpPower = 0;


float s0_temperature = 0;
float s1_temperature = 0;
byte readFromSensor = 0xFF;

// Prototypes
void i2c_received_handler(int count);
void i2c_request_handler(int count);
float read_temp(void);
float read_avg_temp(int count);


/**
* Setup the Arduino
*/
void setup(void){
	// Configure I2C to run in slave mode with the defined address
	Wire.begin(I2C_SLAVE_ADDR);

	// Received I2C data handler
	Wire.onReceive(i2c_received_handler);

	// Configure the handler for request of data via I2C
	Wire.onRequest(i2c_request_handler);

	// Configure ADC to use voltage reference from AREF pin (external)
	analogReference(EXTERNAL);

	// Setup the serial port to operate at 56.6kbps
	Serial.begin(9600);
	// Serial.begin(56600);

	// Setup board led
	pinMode(BOARD_LED, OUTPUT);
}

/**
* Handles data requests received via the I2C bus
* It will immediately reply with the power stored
*/
void i2c_request_handler(){

	float temp = 0.0;

	if (readFromSensor == 0) {
		temp = s0_temperature;
	} else if (readFromSensor == 1) {
		temp = s1_temperature;
	}

	Wire.write((byte*) &temp, sizeof(float));

	readFromSensor = 0xFF;	// reset
}

/**
* Handles received data via the I2C bus in a form of (device_id: int, value: float)
* Value is asigned to device variable.
*/
void i2c_received_handler(int count){
	if (count == 1) {
		readFromSensor = Wire.read();
	} else if (count == 5) {
		byte device_code = Wire.read();

		union {
			byte b[4];
			float f;
		} data;

		for (int i = 0; i < 4; i++) {
			data.b[i] = Wire.read();
		}

		float value = data.f;

		switch (device_code) {

			case 1:	// Light device
				lightPower = value;
				break;
			case 2: // Fan
				fanPower = value;
				break;
			case 3: // WaterPump
				pumpPower = value;
				break;
			default:
				break;

		}
	}
}

/**
* Reads temperature in C from the ADC
*/
float read_temp(int sensor_id){
  int vplus;
  int vminus;
	if (sensor_id == 0) {
		vplus  = analogRead(0);
		// The reference temperature value, i.e. 0°C
		vminus = analogRead(1);
	} else if (sensor_id == 1) {
		vplus  = analogRead(2);
		// The reference temperature value, i.e. 0°C
		vminus = analogRead(3);
	}

	// Calculate the difference. when V+ is smaller than V- we have negative temp
	int vdiff = vplus - vminus;

	// Temp = vdiff * VAREF / (1024 * 0.01)
	return vdiff * VAREF / 10.24f;
}

/**
* Gets the average of N temperature reads
*/
float read_avg_temp(int count, int sensor_id){
	float avgtemp = 0;
	for(int i = 0; i < count; ++i)
		avgtemp += read_temp(sensor_id);

	return avgtemp / count;
}



void loop(){
	s0_temperature = read_temp(0);
	s1_temperature = read_temp(1);

	Serial.print("Sensor 0 --> ");
	Serial.println(s0_temperature);

	Serial.print("Sensor 1 --> ");
	Serial.println(s1_temperature);


	delay(100);
}
