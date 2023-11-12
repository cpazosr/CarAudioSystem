// Autores:
// Manuel Agustin Diaz Vivanco
// Carlos Antonio Pazos Reyes

#include <IRremote.h>
#include <Wire.h> 
#include <DHT.h>

//infra 
const int RECV_PIN = 22;

IRrecv irrecv(RECV_PIN);
//IRrecv irrecv;
decode_results results;
unsigned long key_value = 0;

//Botones play/pause, next, prev
const int play = 51;
const int next = 50;
const int prev = 52;

//sensor DHT11 temp y hum
const int DHTPIN = 32;
//Inicializamos el sensor  DHTT11
DHT dht(DHTPIN, DHT11);

//Rotary encoder 
const int outputA = 26; //CLK
const int outputB = 27; //DT
const int swch = 28;
int volumen = 0;
int aState;
int aLastState;

//Calendario con horas,min y seg 
// Declaracion de las variables para almacenar informacion de tiempo leida desde RTC
uint8_t second, minute, hour, wday, day, month, year, ctrl;
int min_ant;


void setup(){
  Serial.begin(9600);
  irrecv.enableIRIn();
  //irrecv.begin(RECV_PIN, ENABLE_LED_FEEDBACK);
  
  //Botones en pullup para evitar fallos al iniciar
  pinMode(play, INPUT_PULLUP);
  pinMode(next, INPUT_PULLUP);
  pinMode(prev, INPUT_PULLUP);
  
  //sens temp y humedad
  dht.begin();
  
  //Rotary encoder
  pinMode(outputA,INPUT);
  pinMode(outputB,INPUT);
  pinMode (swch, INPUT_PULLUP);
  //leemos el estado inicial del encoder 
  aLastState = digitalRead(outputA);

  //Setup Calendario con horas,min y seg 
  // Preparar la librería Wire (I2C)
  Wire.begin();
  
  
}

void loop(){
  // Iniciamos lectura de la distancia
 
  // lectura de botones 
  if (digitalRead(play) == LOW){
    Serial.println("Button:play");
    //Serial.println("\n");
    delay(500);
  }
  else if (digitalRead(next) == LOW){
    Serial.println("Button:next");
    //Serial.println("\n");
    delay(500);
  }
  else if (digitalRead(prev) == LOW){
    Serial.println("Button:prev");
    //Serial.println("\n");
    delay(500);
  }
  
  if (irrecv.decode(&results)){
         
        if (results.value == 0XFFFFFFFF){
           
           results.value = key_value;
        }
        
        switch(results.value){
          case 0xFFA25D:
          Serial.println("IR:OFF");
          break;
          case 0xFF629D:
          Serial.println("IR:Mode");
          break;
          case 0xFFE21D:
          Serial.println("IR:Mute");
          break;
          case 0xFF22DD:
          Serial.println("IR:>=");
          break;
          case 0xFF02FD:
          Serial.println("IR:|<<");
          break ;  
          case 0xFFC23D:
          Serial.println("IR:>>|");
          break ;               
          case 0xFFE01F:
          Serial.println("IR:EQ");
          break ;  
          case 0xFFA857:
          Serial.println("IR:-");
          break ;  
          case 0xFF906F:
          Serial.println("IR:+");
          break ;  
          case 0xFF6897:
          Serial.println("IR:0");
          break ;  
          case 0xFF9867:
          Serial.println("IR:100+");
          break ;
          case 0xFFB04F:
          Serial.println("IR:200+");
          break ;
          case 0xFF30CF:
          Serial.println("IR:1");
          break ;
          case 0xFF18E7:
          Serial.println("IR:2");
          break ;
          case 0xFF7A85:
          Serial.println("IR:3");
          break ;
          case 0xFF10EF:
          Serial.println("IR:4");
          break ;
          case 0xFF38C7:
          Serial.println("IR:5");
          break ;
          case 0xFF5AA5:
          Serial.println("IR:6");
          break ;
          case 0xFF42BD:
          Serial.println("IR:7");
          break ;
          case 0xFF4AB5:
          Serial.println("IR:8");
          break ;
          case 0xFF52AD:
          Serial.println("IR:9");
          break ;     
          default:
          NULL;
          break; 
        }
        key_value = results.value;
        delay(250);
        irrecv.resume(); 
        
  }
  
  //Rotary encoder 
  // leemos la posicion actual 
  aState = digitalRead(outputA); 
  // si el estado anterior y el actual son diferentes, ocurrio un pulso 
  if (aState != aLastState){
    // si el outputB es distinto al outputA,se gira a la derecha
    if (digitalRead(outputB) != aState){ 
      volumen = 1;
    } else{
      volumen = -1;
    }
    Serial.print("Volumen:");
    Serial.print(volumen);
    Serial.println("");
  }
  aLastState = aState;

  //Calendario 
  // Leer los registros del RTC
  
  if (read_ds1307()) {
    // Mostrar la fecha y hora
    if ( minute != min_ant){
        print_time();
        min_ant = minute;


        //Leemos la humedad
        int hum = dht.readHumidity();
        int temp = dht.readTemperature();
        //checamos errores en la lectura
        if (isnan(hum) || isnan(temp)) {
          Serial.println("Error obteniendo los datos del sensor DHT11");
          return;
        }  
        //sens temperatura y hum
        // Calcular el índice de calor en grados centígrados
        int hic = dht.computeHeatIndex(temp, hum, false);
        
        Serial.print("DHT:");
        //Serial.print("Humedad:");
        Serial.print(hum);
        Serial.print("%,");
        //Serial.print("Temperatura:");
        Serial.print(temp);
        Serial.print("°C,");
        //Serial.print("Indice de calor:");
        Serial.print(hic);
        Serial.println("°C");   
        //Serial.println();

      }
    }
   else {
    // No se puede leer desde le DS1307 (NACK en I2C)
    Serial.println("No se detecta el DS1307, revisar conexiones");
  }
}

bool read_ds1307()
{
  // Iniciar el intercambio de información con el DS1307 (0xD0)
  Wire.beginTransmission(0x68);
 
  // Escribir la dirección del segundero
  Wire.write(0x00);
 
  // Terminamos la escritura y verificamos si el DS1307 respondio
  // Si la escritura se llevo a cabo el metodo endTransmission retorna 0
  if (Wire.endTransmission() != 0)
    return false;
 
  // Si el DS1307 esta presente, comenzar la lectura de 8 bytes
  Wire.requestFrom(0x68, 8);
 
  // Recibimos el byte del registro 0x00 y lo convertimos a binario
  second = bcd2bin(Wire.read());
  minute = bcd2bin(Wire.read()); // Continuamos recibiendo cada uno de los registros
  hour = bcd2bin(Wire.read());
  wday = bcd2bin(Wire.read());
  day = bcd2bin(Wire.read());
  month = bcd2bin(Wire.read());
  year = bcd2bin(Wire.read());
 
  // Recibir los datos del registro de control en la dirección 0x07
  ctrl = Wire.read();
 
  // Operacion satisfactoria, retornamos verdadero
  return true;
}
 
/**
   Esta función convierte un número BCD a binario. Al dividir el número guardado
   en el parametro BCD entre 16 y multiplicar por 10 se convierten las decenas
   y al obtener el módulo 16 obtenemos las unidades. Ambas cantidades se suman
   para obtener el valor binario.
*/
uint8_t bcd2bin(uint8_t bcd)
{
  // Convertir decenas y luego unidades a un numero binario
  return (bcd / 16 * 10) + (bcd % 16);
}
 
/**
   Imprime la fecha y hora al monitor serial de arduino
*/
void print_time()
{     
    Serial.print("UTC:");
    //Serial.print("Fecha:");
    Serial.print(day);
    Serial.print('/');
    Serial.print(month);
    Serial.print('/');
    Serial.print(year);
   
    //Serial.print(" Hora:");
    Serial.print(",");
    Serial.print(hour);
    Serial.print(':');
    Serial.println(minute);
   
    //Serial.println();
  }
