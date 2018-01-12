#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
int outPin = 8; 
int up = 95;
int down = 7; 
int backlight = 7;
Servo flag;
String readString = "";
String previousString;
String user = "Logged in";
String previousUser = "Logged in";

int button = 9;
boolean currentButton = LOW;

String line1 = "";
String line2 = "";

void setup()
{
  pinMode(button, INPUT);
  line1 = "Please Log In";
  int bl_delay = 800;
  Serial.begin(9600);
  Serial.flush();
  flag.attach(outPin);
  flag.write(down);
  pinMode(backlight, OUTPUT);
  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.print(line1);
  
  for (int i = 0; i < 4; i++)
    {
      digitalWrite(backlight, HIGH);
      delay(bl_delay);
      digitalWrite(backlight, LOW);
      delay(bl_delay);
    }
  
  lcd.clear(); 
  }

void loop()

{
  int bl_delay = 3500;
  while (Serial.available())
  {
     delay(10);
     char c = Serial.read();
      
      if (c == ',')
      {
        break;
      }
      
      if (c == '>')
      {
        user = readString;
        readString = "";
        Serial.println(user);
        break;
      }
       readString += c;   
  }
  
  
  if (digitalRead(button) == HIGH) 
  {
    delay(60);
    if (digitalRead(button) == HIGH)
    {
      currentButton = HIGH;
     }
  }
    
  if (currentButton == HIGH)
  {
    lcd.setCursor(0,0);
    lcd.print(line1);
    lcd.setCursor(0,1);
    lcd.print(line2);
    digitalWrite(backlight, HIGH);
    currentButton = LOW;
    delay(5000);
    digitalWrite(backlight, LOW);
    lcd.clear();
  }
  
  
  if(readString.length() > 0)
  {
    Serial.print(readString);
    
    // Handles a strange glitch where the string will sometimes be read as "No" and sometimes read as "N" and then "o".  
    if (readString.charAt(0) == 'N' || readString.charAt(0) == 'o')
    {
      readString = "No";
    }
    
    if (readString == "No")
    {
      Serial.println(" new messages.");
      flag.write(down);
      line1 = user + ":";
      line2 = readString + " new messages.";
    }
        
        
    else if (readString == "One more")
    {
      Serial.println(" new message!");
      flag.write(down);
      delay(700);
      flag.write(up);
     }
        
        
     else if (readString == "1")
     {
       flag.write(up);
       Serial.println(" new message!");
       line1 = user + ":";
       line2 = readString + " new message!";
      }
        
        
       else if (readString == "Log out")
       {
         flag.write(down);
         lcd.clear();
         lcd.print("Logged out");
         digitalWrite(backlight, HIGH);
         delay(bl_delay);
         lcd.clear();
         line1 = "Please Log In";
         line2 = "";
        }
        
        else
        {
          flag.write(up);
          Serial.println(" new messages!");
          line1 = user + ":";
          line2 = readString + " new messages!";
         }
        
        
        if (previousString != readString  && readString != "One more")
        {
          lcd.setCursor(0,0);
          lcd.print(line1);
          lcd.setCursor(0,1);
          lcd.print(line2);
          digitalWrite(backlight, HIGH);
          delay(bl_delay);
          digitalWrite(backlight, LOW);
          lcd.clear();
          previousString = readString;
        }
        
        
        if (previousUser != user )
        {
          lcd.setCursor(0,0);
          lcd.print(line1);
          lcd.setCursor(0,1);
          lcd.print(line2);
          digitalWrite(backlight, HIGH);
          delay(bl_delay);
          digitalWrite(backlight, LOW);
          lcd.clear();
          previousUser = user;
        }
        
        readString = "";
      }
  }
