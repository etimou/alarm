#include <HRCSwitch.h>

int recepteurPin = 2;
char rchar;
char rstring[32];
int rindex;

struct config_t
{
  long sender;
  int receptor;
} signal;

struct signal_t
{
  long sender;
  int receptor;
  boolean isSignal;
  boolean state;
} receivedSignal;

HRCSwitch mySwitch = HRCSwitch();

void setup() {
  
  pinMode(2, INPUT);
  pinMode(10, OUTPUT);//acoustic alarm
  pinMode(12, OUTPUT);
  Serial.begin(9600);
  mySwitch.enableReceive(0);  // Receiver on inerrupt 0 => that is pin #2
  mySwitch.enableTransmit(12);
}

void loop() {
  if (mySwitch.available()) {
    
    int value = mySwitch.getReceivedValue();
    
    if (value == 0) {
      Serial.print("Unknown encoding");
    } else {
      Serial.print("Received ");
      Serial.println( mySwitch.getReceivedValue() );
      //Serial.print(" / ");
      //Serial.print( mySwitch.getReceivedBitlength() );
      //Serial.print("bit ");
      //Serial.print("Protocol: ");
      //Serial.println( mySwitch.getReceivedProtocol() );
    }

    mySwitch.resetAvailable();
  }

   if (Serial.available() > 0) {
     rchar = Serial.read();
     if (rchar != '\n' && rindex<32)
     {
       rstring[rindex] = rchar;
       rindex++;
     }
     else
     {
            rstring[rindex] = 0;
            strcpy(rstring,(strstr(rstring, "CMD")));
            if (strlen(rstring)>4)
            {
              //command detected
              //Serial.println("New Command");
              //Serial.println(rstring);
              char IDrecipient[16];
              for (int i=0; i<16; i++)
              {
                IDrecipient[i]=rstring[i+4];
                if (IDrecipient[i]==' ')
                {
                  IDrecipient[i]=0;
                  strcpy(rstring, rstring+i+5);
                  break;
                }
              }
              
              bool status_receiver =0;
              if (rstring[0]=='1') status_receiver=1;
              
              //Serial.print("Rec: ");
              //Serial.println(IDrecipient);
              //Serial.print("Sta: ");
              //Serial.println(status_receiver);
              
              unsigned long IDR=atol(IDrecipient);
              
              //Serial.println(IDR);
              if (IDR==1981)
              {
                 digitalWrite(10, status_receiver);
              }
              else
              {
                mySwitch.send(IDR,1,status_receiver);
              }
                 
            }
            else
            {
              Serial.println("OK");
            }
       rindex=0;
     }

        

        //mySwitch.send(11985906,1,data);

   } 
   
}


