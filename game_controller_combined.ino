/*
 * Combined Game Controller - Joystick + Ultrasonic Sensor
 * For Log Roller Game with Arduino Controls
 * 
 * Hardware Setup:
 * - Ultrasonic Sensor HC-SR04:
 *   - VCC -> 5V
 *   - GND -> GND
 *   - Trig -> Pin 9
 *   - Echo -> Pin 10
 * 
 * - Analog Joystick:
 *   - VCC -> 5V
 *   - GND -> GND
 *   - VRx -> A2 (X-axis)
 *   - VRy -> A3 (Y-axis)
 *   - SW -> A4 (Button)
 */

// Ultrasonic Sensor Pins
const int trigPin = 9;
const int echoPin = 10;

// Joystick Pins
#define ANALOG_X_PIN A2 
#define ANALOG_Y_PIN A3 
#define ANALOG_BUTTON_PIN A4 

// Joystick calibration values
#define ANALOG_X_CORRECTION 128 
#define ANALOG_Y_CORRECTION 128 

// Variables for sensor readings
float duration, distance;
int joystick_x, joystick_y;
bool button_pressed;

void setup() {
  // Initialize ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Initialize joystick button pin
  pinMode(ANALOG_BUTTON_PIN, INPUT_PULLUP);
  
  // Start serial communication at 115200 baud
  // (matching the baudrate in arduino_controls.py)
  Serial.begin(115200);
  
  // Give time for serial connection to establish
  delay(1000);
  Serial.println("Game Controller Ready!");
}

void loop() {
  // Read ultrasonic sensor
  readUltrasonicSensor();
  
  // Read joystick
  readJoystick();
  
  // Send all data in the format expected by arduino_controls.py
  sendSensorData();
  
  // Small delay to avoid overwhelming the serial connection
  delay(50);  // 20 readings per second
}

void readUltrasonicSensor() {
  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read the echo duration
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate distance in centimeters
  distance = (duration * 0.0343) / 2;
  
  // Limit distance readings to reasonable range
  if (distance > 400) {
    distance = 400;  // Max reasonable distance
  }
}

void readJoystick() {
  // Read raw analog values first (for debugging)
  int raw_x = analogRead(ANALOG_X_PIN);
  int raw_y = analogRead(ANALOG_Y_PIN);
  
  // Map to 0-255 range
  byte mapped_x = map(raw_x, 0, 1023, 0, 255);
  byte mapped_y = map(raw_y, 0, 1023, 0, 255);
  
  // Apply correction
  joystick_x = mapped_x - ANALOG_X_CORRECTION;
  joystick_y = mapped_y - ANALOG_Y_CORRECTION;
  
  // Debug output (comment out after fixing)
  Serial.print("DEBUG_RAW: X=");
  Serial.print(raw_x);
  Serial.print(" Y=");
  Serial.print(raw_y);
  Serial.print(" | MAPPED: X=");
  Serial.print(mapped_x);
  Serial.print(" Y=");
  Serial.print(mapped_y);
  Serial.print(" | CORRECTED: X=");
  Serial.print(joystick_x);
  Serial.print(" Y=");
  Serial.println(joystick_y);
  
  // Read button state
  button_pressed = isAnalogButtonPressed(ANALOG_BUTTON_PIN);
}

void sendSensorData() {
  // Send data in the exact format expected by arduino_controls.py
  
  // Joystick X
  Serial.print("X:");
  Serial.println(joystick_x);
  
  // Joystick Y  
  Serial.print("Y:");
  Serial.println(joystick_y);
  
  // Button state
  if (button_pressed) {
    Serial.println("Button pressed");
  } else {
    Serial.println("Button not pressed");
  }
  
  // Ultrasonic distance
  Serial.print("Distance:");
  Serial.println(distance);
}

// Helper function to map analog reading to 0-255 range
byte readAnalogAxisLevel(int pin) {
  return map(analogRead(pin), 0, 1023, 0, 255);
}

// Helper function to check if button is pressed
bool isAnalogButtonPressed(int pin) {
  return digitalRead(pin) == 0;  // Button pulled low when pressed
}
