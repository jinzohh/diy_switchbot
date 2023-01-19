#include <Wire.h>
#include <AFMotor.h> //Make sure Adafruit Motorshield library is installed

AF_DCMotor motor(2, MOTOR12_64KHZ); // motor M2, 64KHz pwm

int r = 0;
int r_prev = 0;

void moveForward()
{
    motor.run(FORWARD);
}

void moveBackward()
{
    motor.run(BACKWARD);
}

void motorStop()
{
    motor.run(RELEASE);
}

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    delay(10);
    motor.setSpeed(200); // 255 is max
}

void loop() {
    // put your main code here, to run repeatedly:
    if(Serial.available())
    {
        r = Serial.read() - '0';

        if(r != r_prev)
        {
            moveForward();
            delay(500); //This rotates the motor forward for 500ms
            motorStop();
            delay(10); //This gives a 10ms break before rotating in the opposite direction
            moveBackward();
            delay(440); //This rotates the motore backward for 440ms
            motorStop();

            r_prev = r; //This saves the last r value
        }
        else{
            motorStop();
        }
    }
}