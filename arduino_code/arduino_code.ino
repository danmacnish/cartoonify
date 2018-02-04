#include <TimerOne.h>
#include <Bounce.h>
#include "arduino_code.h"


volatile states state;
const int LED_PIN  = 13;  
const int POWER_BUTTON = 2; //low when power button pressed
const int RPI_POWER_PIN = 12;  //set this high to switch optocoupler and turn rpi on/off

unsigned long start_time = 0;
volatile int ledState = LOW;
Bounce power_button = Bounce(POWER_BUTTON, 50);

void setup() {
  Serial.begin(9600);
  state = powering_up;
  pinMode(LED_PIN, OUTPUT);
  pinMode(RPI_POWER_PIN, OUTPUT);
  pinMode(POWER_BUTTON, INPUT_PULLUP);
  digitalWrite(RPI_POWER_PIN, HIGH);
  Timer1.initialize(500000);
  Timer1.attachInterrupt(blinkLED);
}

void loop() {
  power_button.update();
  Serial.print("power button: ");
  Serial.print(power_button.read());
  Serial.print(" state: ");
  Serial.println(state);
  if (state == powering_up && millis() - start_time > 25000) {
    state = on;
  } else if (state == powering_down && millis() - start_time > 20000) {
    state = off;
  } else if (!power_button.read() && power_button.duration() > 1500 && state == on) {
    state = powering_down;
    start_time = millis();
    pulse_rpi();
  } else if (!power_button.read() && power_button.duration() > 1500 && state == off) {
    state = powering_up;
    start_time = millis();
    pulse_rpi();
  }
}

void blinkLED(void)
{
  if (ledState == LOW) {
    ledState = HIGH;
  } else {
    ledState = LOW;
  }
  if (state == powering_up || state == powering_down) {
    digitalWrite(LED_PIN, ledState);
  } else if (state == on) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}

void pulse_rpi(void) {
  // pulse raspi on pin
  digitalWrite(RPI_POWER_PIN, LOW);
  delay(500);
  digitalWrite(RPI_POWER_PIN, HIGH);
}

