uint8_t bytes_buffer[10];
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    Serial.readBytesUntil((char)200, bytes_buffer, 3);
  }
}
