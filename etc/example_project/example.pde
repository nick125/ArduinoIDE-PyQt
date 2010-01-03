

const int pinRed = 12;

void setup()
{
	//* set ports
	pinMode(pinRed, OUTPUT);
	//pinMode(pinYellow, OUTPUT);
	//pinMode(pinGreen, OUTPUT);
	
	//MsTimer2::set(1000, flash);
	//MsTimer2::set(500, flash_off);
	//MsTimer2::start();
	
	//Serial.begin(9600);
	
	//* Attch callback to mesage
	//message.attach(message_ready);
}

void loop()
{
	digitalWrite(pinRed, HIGH);
	delay(500);
	digitalWrite(pinRed, LOW);
	delay(500);
}

