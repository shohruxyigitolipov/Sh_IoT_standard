// device_client_cpp.ino — главный файл

#include "wifi_manager.h"
#include "time_manager.h"
#include "PinController.h"
#include "websocket_manager.h"

// Wi-Fi и WebSocket настройки
const char* SSID = "Galaxy";
const char* PASSWORD = "60533185";
const char* WS_URL = "wss://shiotstandard-production.up.railway.app:443/devices/ws/1/connect";
const String AUTH_TOKEN = "{\"auth_token\":\"abc123\"}";

// Пины управления
const int CONTROL_PINS[] = {4, 5, 12, 13, 14};
const size_t PIN_COUNT = sizeof(CONTROL_PINS) / sizeof(CONTROL_PINS[0]);

WiFiManager wifi(SSID, PASSWORD);
TimeManager timeManager(5 * 3600); // GMT+5
PinController pinController;
WebSocketManager wsManager(pinController);  // ✅ передаём контроллер

unsigned long lastTimeSync = 0;
unsigned long lastScheduleCheck = 0;

void setup() {
  Serial.begin(115200);
  wifi.connect();
  timeManager.begin();
  pinController.setup(CONTROL_PINS, PIN_COUNT);

  wsManager.connect(WS_URL, AUTH_TOKEN); // ✅ без onMessage
}

void loop() {
  wsManager.loop();
  wifi.ensureConnection();

  unsigned long now = millis();

  if (now - lastTimeSync > 60000) {
    timeManager.sync();
    lastTimeSync = now;
  }

  if (now - lastScheduleCheck > 1000) {
  auto changedPins = pinController.handleAutoLogic();
  for (int pin : changedPins) {
    wsManager.send(pinController.generateReport(pin));  // отправка отчёта по каждому
  }
  lastScheduleCheck = now;
}


  if (!wsManager.isConnected()) {
    wsManager.connect(WS_URL, AUTH_TOKEN);
  }
}