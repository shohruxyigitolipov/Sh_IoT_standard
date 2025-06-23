// WiFiManager.h
#pragma once

#include <ESP8266WiFi.h>

class WiFiManager {
public:
    WiFiManager(const char* ssid, const char* password)
        : ssid_(ssid), password_(password) {}

    void connect() {
        WiFi.begin(ssid_, password_);
        Serial.print("Connecting to Wi-Fi");
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }
        Serial.println(" connected!");
    }

    void ensureConnection() {
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("Wi-Fi lost, reconnecting...");
            connect();
        }
    }

private:
    const char* ssid_;
    const char* password_;
};