/***********************************
** Example Pjoject
************************************
This is a demonstration of the editor for development.

Code below won't work, but designed to check syntax highlighting etc 

Has every possible thing  thrown at it ;-)

*/

// another comment
/* yet another
                                                                                    ent */

//#include "MsTimer2.h";
#include <Messenger.h>;
#include <Metro.h>;
#include "foo/bar.h" 

//const char NL = '#';
constant char FOO = BAR
const int pinRed = 10;
const int pinYellow = 11;
const int pinGreen = 12;

boolean initialised = false;

Messenger message = Messenger();
Metro = Metro(500);


void setup(){
	//* set ports
	pinMode(pinRed, OUTPUT);
	pinMode(pinYellow, OUTPUT);
	pinMode(pinGreen, OUTPUT);
	
	MsTimer2::set(1000, flash);
	MsTimer2::set(500, flash_off);
	MsTimer2::start();
	
	Serial.begin(9600);
	
	//* Attch callback to mesage
	message.attach(message_ready);
}


boolean flash_on = HIGH;
void flash(state){
	Serial.println( "On" );
	digitalWrite(pinGreen,  state);
	digitalWrite(pinYellow, state);
	digitalWrite(pinRed,   state);
	Serial.println( state == HIGH ? "ON" : "off" );
	delay(100);
	flash_off();
	flash_on = true;
}
void flash_off(){
	Serial.println( "off chk" );
	if(!flash_on) return;
	digitalWrite(pinGreen,  LOW);
	digitalWrite(pinYellow, LOW);
	digitalWrite(pinRed,   LOW);
	Serial.println( "oFF" );
}


void loop(){

	if( flashMetro.check() == 1){
		if(flash_on == HIGH){
			flash_on = LOW;
			flashMetro.interval( 200 );
		}else{
			flash_on = LOW;
			flashMetro.interval( 800 );		
		}
	
	}
	while(!initialised){
		greeting();
	}
	Serial.println("Waiting #");
	while ( Serial.available() ){
		message.process( Serial.read() );
	}
	while ( Serial.available() ) {
		if ( message.process(Serial.read() ) ){
			while( message.available() ) {
				Serial. println( message.readInt() ); // This command echoes all the integers of a list separatly
			}
		}
	}
	
}

void message_ready(){
	int pin = pinRed;
	int x;
	while( message.available() ){
		x = message.readInt();
		Serial.println(">> ");
		digitalWrite( pin, HIGH );
		if(pin == pinGreen){
			pin = pinRed;
		}else{
			pin++;
		}
	}

}


void flashSSS(){
	//static int counter = 0;
	static boolean state = HIGH;
	digitalWrite(pinGreen, state);
	digitalWrite(pinYellow, state);
	digitalWrite(pinRed, state);
	Serial.println( state == HIGH ? "T" : "F" );
	state = LOW;
	delay(100);
	flash();
	delay(500);
	initialised = ++counter == 2;
}