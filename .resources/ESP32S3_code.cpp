#include <ESP8266WiFi.h>
#include <ArduinoWebsockets.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include <ArduinoJson.h>
#include <map>

using namespace websockets;

// ——— Wi-Fi настройки ————————————————————————
const char* ssid     = "Galaxy";
const char* password = "60533185";

// ——— WebSocket ————————————————————————————————
const char* ws_url = "wss://shiotstandard-production.up.railway.app:443/devices/ws/1/connect";
WebsocketsClient client;
bool wsConnected = false;
String auth_token = "{\"auth_token\":\"abc123\"}";

// ——— NTP (GMT+5 Узбекистан) ————————————————————
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 5 * 3600, 60000);

// ——— Пины ————————————————————————————————
const int pinList[] = {4, 5, 12, 13, 14};

struct PinConfig {
  String mode = "manual";
  String on_time = "12:00";
  String off_time = "13:00";
};

std::map<int, PinConfig> pins;

// ——— Подключение к Wi-Fi ————————————————————————
void connectWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected!");
}

// ——— Синхронизация времени ————————————————————————
void syncTime() {
  if (timeClient.update()) {
    setTime(timeClient.getEpochTime());
    Serial.print("Time: ");
    Serial.println(timeClient.getFormattedTime());
  }
}
void sendReport(int pin = -1) {

  StaticJsonDocument<512> doc;
  doc["type"] = "report";
  JsonArray pin_list = doc.createNestedArray("pin_list");

  if (pin == -1) {
    // Отправить все пины
    for (auto& entry : pins) {
      int p = entry.first;
      PinConfig& cfg = entry.second;

      JsonObject item = pin_list.createNestedObject();
      item["pin"] = p;
      item["state"] = digitalRead(pin);
      item["mode"] = cfg.mode;
      item["schedule"]["on_time"] = cfg.on_time;
      item["schedule"]["off_time"] = cfg.off_time;
    }
  } else {
    // Только один пин
    if (pins.count(pin)) {
      PinConfig& cfg = pins[pin];
      JsonObject item = pin_list.createNestedObject();
      item["pin"] = pin;
      item["state"] = digitalRead(pin);
      item["mode"] = cfg.mode;
      item["schedule"]["on_time"] = cfg.on_time;
      item["schedule"]["off_time"] = cfg.off_time;
    }
  }

  String jsonStr;
  serializeJson(doc, jsonStr);

  client.send(jsonStr);
  Serial.print("To WS: ");Serial.println(jsonStr);
}


// ——— Обработка входящих команд ————————————————————
void handleCommand(const String& msg) {
  StaticJsonDocument<512> doc;
  DeserializationError err = deserializeJson(doc, msg);
  if (err) {
    Serial.print("JSON parse error: ");
    Serial.println(err.c_str());
    return;
  }

  const char* action = doc["action"];
  if (!action) return;

  int pin = doc["pin"] | -1;

  if (strcmp(action, "set_state") == 0 && pin != -1) {
    int state = doc["state"];
    pinMode(pin, OUTPUT);
    digitalWrite(pin, state);
    Serial.printf("Pin %d set to %d\n", pin, state);
    sendReport(pin);
  }
  else if (strcmp(action, "set_mode") == 0 && pin != -1) {
    String mode = doc["mode"] | "manual";
    pins[pin].mode = mode;
    Serial.printf("Pin %d mode set to %s\n", pin, mode.c_str());
    sendReport(pin);
  }
  else if (strcmp(action, "set_schedule") == 0 && pin != -1) {
    pins[pin].on_time = doc["schedule"]["on_time"] | "12:00";
    pins[pin].off_time = doc["schedule"]["off_time"] | "13:00";
    Serial.printf("Pin %d schedule updated\n", pin);
    sendReport(pin);
  }
  else if (strcmp(action, "report") == 0) {
    sendReport();
  }
}

// ——— Настройка WebSocket ————————————————————————
void setupWebsocket() {
  client.onEvent([](WebsocketsEvent evt, String data) {
    switch (evt) {
      case WebsocketsEvent::ConnectionOpened:
        Serial.println("WS connected");
        wsConnected = true;
        break;
      case WebsocketsEvent::ConnectionClosed:
        Serial.println("WS disconnected");
        wsConnected = false;
        break;
      default: break;
    }
  });

  client.onMessage([](WebsocketsMessage msg) {
  String data = msg.data();
  Serial.print("WS msg: ");
  Serial.println(data);

  // 🔁 ping-поддержка
  if (data == "ping") {
    client.send("pong");
    Serial.println("🔁 Received ping → sent pong");
    return;
  }

  handleCommand(data);
});


  Serial.print("Connecting WS… ");
  if (client.connect(ws_url)) {
    Serial.println("OK");
    client.send(auth_token);
  } else {
    Serial.println("Failed");
  }
}

// ——— setup() ————————————————————————————————————————
void setup() {
  Serial.begin(115200);
  connectWiFi();
  syncTime();

  for (int pin : pinList) {
    pins[pin] = PinConfig();  // default
    pinMode(pin, OUTPUT);
    digitalWrite(pin, 0);
  }

  setupWebsocket();
}

// ——— loop() ———————————————————————————————————————————
void loop() {
  client.poll();

  static unsigned long lastSync = 0;
  if (millis() - lastSync > 60000) {
    syncTime();
    lastSync = millis();
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi lost, reconnecting...");
    connectWiFi();
    syncTime();
  }

  if (!wsConnected) {
    Serial.println("Reconnecting WS…");
    if (client.connect(ws_url)) {
      Serial.println("WS reconnected");
      client.send(auth_token);
    } else {
      Serial.println("WS reconnect failed");
    }
  }

  // 🔁 Автоматическое управление по расписанию
  static unsigned long lastScheduleCheck = 0;
  if (millis() - lastScheduleCheck > 1000) {
    lastScheduleCheck = millis();

    int currentHour = hour();
    int currentMinute = minute();
    int nowMins = currentHour * 60 + currentMinute;

    for (auto& entry : pins) {
      int pin = entry.first;
      PinConfig& cfg = entry.second;

      if (cfg.mode != "auto") continue;

      int onH, onM, offH, offM;
      sscanf(cfg.on_time.c_str(), "%d:%d", &onH, &onM);
      sscanf(cfg.off_time.c_str(), "%d:%d", &offH, &offM);

      int onMins = onH * 60 + onM;
      int offMins = offH * 60 + offM;

      bool isOn = (onMins < offMins)
                    ? (nowMins >= onMins && nowMins < offMins)
                    : (nowMins >= onMins || nowMins < offMins);

      int newState = isOn ? 1 : 0;

      if (newState != cfg.state) {
        cfg.state = newState;
        digitalWrite(pin, newState);
        Serial.printf("Auto control: Pin %d set to %d\n", pin, newState);
        sendReport();
      }
    }
  }
}