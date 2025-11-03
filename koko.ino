/*
  KOKO_EmotionTest.ino
  ---------------------
  Use this to manually test KOKO robot’s motion system from the Serial Monitor.

  Type one of these in the Serial Monitor (set NL & CR, 9600 baud):
    HAPPY
    SAD
    ANGRY
    NEUTRAL
    SURPRISE

  The robot will perform the corresponding action.
*/

#define ENA 5     // PWM Left motor
#define IN1 6
#define IN2 7
#define ENB 3    // PWM Right motor
#define IN3 8
#define IN4 9

String emotion = "";

void setup() {
  Serial.begin(9600);
  Serial.println("=== KOKO Emotion Test ===");
  Serial.println("Type an emotion (HAPPY / SAD / ANGRY / NEUTRAL / SURPRISE)");
  Serial.println("and press ENTER.\n");

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotion();
}

void loop() {
  if (Serial.available() > 0) {
    emotion = Serial.readStringUntil('\n');
    emotion.trim();
    emotion.toUpperCase();
    Serial.print("Emotion received: ");
    Serial.println(emotion);

    if (emotion == "REWARD_LEARNING") {
      actionHappy();
    } 
    else if (emotion == "GENTLE_FORWARD") {
      actionSad();
    } 
    else if (emotion == "SLOW_BACK") {
      actionAngry();
    } 
    else if (emotion == "INTERACTIVE_PROMPT") {
      actionNeutral();
    } 
    else if (emotion == "SHOW_SURPRISED_EYES") {
      actionSurprise();
    } 
    else {
      Serial.println("Unknown emotion! Try again.");
    }
  }
}

/* ---------------- Motor Control ---------------- */

void forward(int speedVal) {
  analogWrite(ENA, speedVal);
  analogWrite(ENB, speedVal);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  
}

void backward(int speedVal) {
  analogWrite(ENA, speedVal);
  analogWrite(ENB, speedVal);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);


}

void spinRight(int speedVal) {
  analogWrite(ENA, speedVal);  // Left motor speed
  analogWrite(ENB, speedVal);  // Right motor speed
  
  // Left motors FORWARD
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  
  // Right motors BACKWARD
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}


void stopMotion() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

/* ---------------- Emotion Actions ---------------- */

void actionHappy() {
  Serial.println("🙂 HAPPY → forward spin + backward spin (fast)");
  spinRight(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
  spinRight(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
  spinRight(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
}

void actionSad() {
  Serial.println("😔 SAD → slow spin");
  spinRight(200);
  delay(1000);
  stopMotion();
}

void actionAngry() {
  Serial.println("😠 ANGRY → slow backward");
  backward(200);
  delay(1000);
  stopMotion();
  backward(200);
  delay(1000);
  stopMotion();
  backward(200);
  delay(1000);
  stopMotion();
}

void actionNeutral() {
  Serial.println("😐 NEUTRAL → stay still");
  stopMotion();
}

void actionSurprise() {
  Serial.println("😲 SURPRISE → quick forward + backward");
  forward(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
  forward(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
  forward(255);
  delay(1000);
  backward(255);
  delay(1000);
  stopMotion();
}
