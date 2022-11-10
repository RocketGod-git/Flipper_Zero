#include "Keyboard.h"

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void setup()
{
  Keyboard.begin();

  delay(500);

 
  delay(1000);

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press(' ');
  Keyboard.releaseAll();

  Keyboard.print("terminal");

  delay(500);

  typeKey(KEY_RETURN);

  delay(4000);

  Keyboard.print("osascript -e 'set volume 7'");

  delay(500);

  typeKey(KEY_RETURN);

  delay(500);

  Keyboard.print("open https://www.youtube.com/watch?v=dQw4w9WgXcQ");

  delay(500);

  typeKey(KEY_RETURN);

  Keyboard.end();
}

void loop() {}
