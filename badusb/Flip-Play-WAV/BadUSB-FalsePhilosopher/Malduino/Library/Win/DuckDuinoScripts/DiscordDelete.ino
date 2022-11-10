#include "Keyboard.h"

void typeKey(int key) {
    Keyboard.press(key);
    delay(50);
    Keyboard.release(key);
}

void setup() {
    Keyboard.begin();

    // Delete i messages
    for (int i = 0; i < 100; i++) {
        // Wait 500ms
        delay(500);

        typeKey(KEY_UP_ARROW);

        delay(200);

        Keyboard.press(KEY_LEFT_CTRL);
        Keyboard.press('a');
        Keyboard.releaseAll();

        delay(200);

        typeKey(KEY_DELETE);

        delay(50);

        typeKey(KEY_RETURN);

        delay(100);

        typeKey(KEY_RETURN);
    }

    // Ending stream
    Keyboard.end();
}

void loop() {

}
