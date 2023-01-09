#include "FastLED.h"
#include "SerialTransfer.h"

SerialTransfer serialTx;

// [ index, red, green, blue]
int32_t ledPrimitives[4];

// An index < 0 denotes an action event.
//  action_key |  action
//      -1     |  clear strip
//      -2     |  set brightness, read from [1]
//      -3     |  set show on write, where false <= 0 < true

CRGB leds[60];

void setup() { 
  FastLED.addLeds<APA102, 4, 5, RGB>(leds, 60);
  Serial.begin(115200);
  serialTx.begin(Serial);
}

bool showOnWrite = true;

void loop() { 
  if(serialTx.available()){
      uint16_t recSize = 0;
      recSize = serialTx.rxObj(ledPrimitives, recSize);
      uint32_t index = ledPrimitives[0];
      if (index < 0) {
        // Apply action
        switch (index) {
          case -1:
            FastLED.clear(true);
            break;
          case -2:
            FastLED.setBrightness(ledPrimitives[1]);
            break;
          case -3:
            showOnWrite = false;
          default:
            break;
        }
      }
      leds[index].r = ledPrimitives[1];
      leds[index].g = ledPrimitives[2];
      leds[index].b = ledPrimitives[3];
      if (showOnWrite) {
        FastLED.show();
      }

      uint16_t sendSize = 0;
      sendSize = serialTx.txObj(ledPrimitives, sendSize);
      serialTx.sendData(sendSize);
  }
}