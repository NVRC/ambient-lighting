#include "FastLED.h"
#include "SerialTransfer.h"

SerialTransfer serialTx;

// [ index, red, green, blue]
int32_t serialMessageBuffer[4];

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
      recSize = serialTx.rxObj(serialMessageBuffer, recSize);
      uint32_t index = serialMessageBuffer[0];
      if (index < 0) {
        // Apply action
        switch (index) {
          case -1:
            FastLED.clear(true);
            break;
          case -2:
            FastLED.setBrightness(serialMessageBuffer[1]);
            break;
          case -3:
            if (serialMessageBuffer[1] > 0){
                showOnWrite = true;
            } else {
                showOnWrite = false;
            }
          default:
            break;
        }
      }
      leds[index].setRGB(serialMessageBuffer[1], serialMessageBuffer[2], serialMessageBuffer[3]);
      if (showOnWrite) {
        FastLED.show();
      }

      uint16_t sendSize = 0;
      sendSize = serialTx.txObj(serialMessageBuffer, sendSize);
      serialTx.sendData(sendSize);
  }
}