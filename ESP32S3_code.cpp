#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ArduinoJson.h>
#include <map>
#include <time.h>

using namespace websockets;

const char* ssid = "Galaxy";
const char* password = "60533185";
const char* websocket_url = "wss://shiotstandard-production.up.railway.app/devices/ws/1/connect";
const char* auth_token = "abc123";

WebsocketsClient client;

unsigned long lastPing = 0;
unsigned long lastTick = 0;
unsigned long lastReconnectAttempt = 0;

struct PinSchedule {
  String on_time;
  String off_time;
};

std::map<int, PinSchedule> schedules;
const int pins[] = {4, 5, 15, 16, 17, 18, 21, 22, 23};
const int numPins = sizeof(pins) / sizeof(pins[0]);

const char* root_ca =
"-----BEGIN CERTIFICATE-----\n"
"MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw\n"
"TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh\n"
"cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4\n"
"WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu\n"
"ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY\n"
"MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc\n"
"h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+\n"
"0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U\n"
"A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW\n"
"T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH\n"
"B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC\n"
"B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv\n"
"KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn\n"
"OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn\n"
"jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw\n"
"qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI\n"
"rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV\n"
"HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq\n"
"hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL\n"
"ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ\n"
"3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK\n"
"NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5\n"
"ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur\n"
"TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC\n"
"jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc\n"
"oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq\n"
"4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA\n"
"mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d\n"
"emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=\n"
"-----END CERTIFICATE-----\n";

void setupPins() {
  for (int i = 0; i < numPins; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }
}

bool isValidTime(const String& t) {
  if (t.length() != 5 || t.charAt(2) != ':') return false;
  int hh = t.substring(0, 2).toInt();
  int mm = t.substring(3, 5).toInt();
  return (hh >= 0 && hh < 24 && mm >= 0 && mm < 60);
}

bool isWithinTimeRange(const String& now, const String& on, const String& off) {
  // Поскольку строки в формате "HH:MM", лексикографическое сравнение корректно
  if (!isValidTime(on) || !isValidTime(off) || !isValidTime(now)) return false;
  if (on <= off) {
    return (now >= on && now < off);
  } else {
    // Диапазон пересекает полночь
    return (now >= on || now < off);
  }
}

void syncTime() {
  // Указываем смещение для Tashkent (UTC+5)
  configTime(5 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Waiting for NTP time sync");
  time_t now = time(nullptr);
  unsigned long start = millis();
  while (now < 24 * 3600) { // если время всё ещё близко к 0 (1970), ждём
    if (millis() - start > 10000) { // таймаут 10 секунд
      Serial.println(" failed (timeout)");
      return;
    }
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println(" done!");
}

void connectWebSocket() {
  client.setCACert(root_ca);
  if (client.connect(websocket_url)) {
    Serial.println("WebSocket connected");
    StaticJsonDocument<128> authDoc;
    authDoc["auth_token"] = auth_token;
    String auth_msg;
    serializeJson(authDoc, auth_msg);
    client.send(auth_msg);
  } else {
    Serial.println("WebSocket connection failed");
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected");

  setupPins();
  syncTime();
  connectWebSocket();

  client.onMessage([](WebsocketsMessage msg) {
    String payload = msg.data();
    payload.trim();
    if (payload.length() == 0 || payload.charAt(0) != '{') {
      // Игнорируем пустые или не JSON-сообщения (ping/pong)
      return;
    }

    lastTick = millis(); // Считаем, что получили сообщение, чтобы не переподключаться
    StaticJsonDocument<512> doc;
    DeserializationError err = deserializeJson(doc, payload);
    if (err) {
      Serial.print("JSON parse error: ");
      Serial.println(err.c_str());
      return;
    }

    const char* action = doc["action"];
    int pin = doc["pin"] | -1;
    int state = doc["state"] | -1;
    String req_id = "";
    if (doc.containsKey("request_id")) {
      req_id = String(doc["request_id"].as<const char*>());
    }

    if (pin < 0) {
      doc.clear();
      return;
    }

    if (strcmp(action, "turn_on") == 0) {
      digitalWrite(pin, HIGH);
      Serial.print(pin);
      Serial.println(" - HIGH");
    }
    else if (strcmp(action, "turn_off") == 0) {
      digitalWrite(pin, LOW);
      Serial.print(pin);
      Serial.println(" - LOW");
    }
    else if (strcmp(action, "set_state") == 0) {
      if (state >= 0) {
        digitalWrite(pin, state ? HIGH : LOW);
        Serial.print(pin);
        Serial.print(" - manual state: ");
        Serial.println(state);
      }
    }
    else if (strcmp(action, "set_schedule") == 0) {
      const char* on_time_c = doc["on_time"];
      const char* off_time_c = doc["off_time"];
      String on_time(on_time_c);
      String off_time(off_time_c);
      if (isValidTime(on_time) && isValidTime(off_time)) {
        schedules[pin] = {on_time, off_time};
        Serial.print("Schedule set for pin ");
        Serial.print(pin);
        Serial.print(": ");
        Serial.print(on_time);
        Serial.print(" - ");
        Serial.println(off_time);
      } else {
        Serial.print("Invalid schedule format for pin ");
        Serial.println(pin);
      }
    }
    else if (strcmp(action, "set_manual") == 0) {
      if (schedules.count(pin)) {
        schedules.erase(pin);
        Serial.print("Manual mode enabled for pin ");
        Serial.println(pin);
      }
      if (state >= 0) {
        digitalWrite(pin, state ? HIGH : LOW);
        Serial.print("Pin ");
        Serial.print(pin);
        Serial.print(" set manual state: ");
        Serial.println(state);
      }
    }

    // Формируем ответ
    doc.clear();
    doc["pin"] = pin;
    doc["status"] = digitalRead(pin);
    if (req_id.length() > 0) {
      doc["request_id"] = req_id;
    }
    String response;
    serializeJson(doc, response);
    client.send(response);
  });
}

void handlePing() {
  if (millis() - lastPing > 10000) {
    // Отправляем текстовый ping - сервер должен на него ответить
    client.send("ping");
    lastPing = millis();
  }
}

void handleSchedule() {
  if (millis() - lastTick > 1000) {
    lastTick = millis();
    time_t rawtime;
    struct tm* timeinfo;
    time(&rawtime);
    timeinfo = localtime(&rawtime);

    char currentTime[6];
    sprintf(currentTime, "%02d:%02d", timeinfo->tm_hour, timeinfo->tm_min);
    String nowStr(currentTime);

    for (auto const& pair : schedules) {
      int pin = pair.first;
      String on_time = pair.second.on_time;
      String off_time = pair.second.off_time;
      if (isWithinTimeRange(nowStr, on_time, off_time)) {
        digitalWrite(pin, HIGH);
      } else {
        digitalWrite(pin, LOW);
      }
    }
  }
}

void handleReconnect() {
  // Попытка переподключения раз в 5 секунд
  if (millis() - lastReconnectAttempt < 5000) return;
  lastReconnectAttempt = millis();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi disconnected. Reconnecting...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    return;
  }

  if (!client.available()) {
    Serial.println("WebSocket disconnected. Reconnecting...");
    connectWebSocket();
  }
}

void loop() {
  if (client.available()) {
    client.poll();
  }
  handlePing();
  handleSchedule();
  handleReconnect();
}

