

const int pinRed = 7;
char x = '';

void setup()
{

	pinMode(pinRed, OUTPUT);

}

void loop()
{
	digitalWrite(pinRed, HIGH);
	delay(400);
	digitalWrite(pinRed, LOW);
	delay(200);
}
