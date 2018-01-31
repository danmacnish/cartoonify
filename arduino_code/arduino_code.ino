#include <TimerOne.h>
#include <Bounce.h>
#include "arduino_code.h"


volatile states state;
const int RPI_ON_PIN = 10;  //low when rpi is on
const int LED_PIN  = 13;  
const int POWER_BUTTON = 2; //low when power button pressed
const int RPI_POWER_PIN = 12;  //set this high to switch optocoupler and turn rpi on/off

volatile int ledState = LOW;
Bounce power_button = Bounce(POWER_BUTTON, 50);
Bounce rpi_on = Bounce(RPI_ON_PIN, 50);

void setup() {
  Serial.begin(9600);
  state = off;
  pinMode(LED_PIN, OUTPUT);
  pinMode(RPI_POWER_PIN, OUTPUT);
  pinMode(RPI_ON_PIN, INPUT);
  pinMode(POWER_BUTTON, INPUT_PULLUP);
  digitalWrite(RPI_POWER_PIN, LOW);
  Timer1.initialize(500000);
  Timer1.attachInterrupt(blinkLED);
}

void loop() {
  rpi_on.update();
  power_button.update();
  Serial.print("rpi on: ");
  Serial.print(rpi_on.read());
  Serial.print(" power button: ");
  Serial.print(power_button.read());
  Serial.print(" state: ");
  Serial.println(state);
  if (rpi_on.read() && (state == powering_up || state == off)) {
    state = on;
  } else if (!rpi_on.read() && rpi_on.duration() > 10000 && state == powering_down) {
      state = off;
  } else if (!power_button.read() && power_button.duration() > 1500 && state == on) {
    state = powering_down;
    pulse_rpi();
  } else if (!power_button.read() && power_button.duration() > 1500 && state == off) {
    state = powering_up;
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
  // pulse the optocoupler to turn the raspi on/off
  digitalWrite(RPI_POWER_PIN, HIGH);
  delay(100);
  digitalWrite(RPI_POWER_PIN, LOW);
}

