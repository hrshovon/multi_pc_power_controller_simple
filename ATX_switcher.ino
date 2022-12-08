uint8_t bytes_buffer[10];
const uint8_t pins[] = {4,5,6,7,8,9,15,14,16,10};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  for(uint8_t i=0;i<10;i++)
  {
    pinMode(pins[i],OUTPUT);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    Serial.readBytesUntil((char)200, bytes_buffer, 3);
    if(bytes_buffer[2] == 150)
    {
      uint8_t pin = bytes_buffer[0];
      uint8_t delay_time = bytes_buffer[1];
      int delay_time_act = 0;
      if(pin<10 && delay_time<10)
      {
        if(delay_time==0)
        {
          delay_time_act = 100;
        }
        else
        {
          delay_time_act = int(delay_time)*1000;
        }
        digitalWrite(pins[pin],HIGH);
        delay(delay_time_act);
        digitalWrite(pins[pin],LOW);
      }
    }
  }
  
}
