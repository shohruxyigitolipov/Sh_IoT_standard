// PinController.h
#pragma once

#include <Arduino.h>
#include <map>
#include <ArduinoJson.h>
#include "TimeLib.h"

struct PinConfig {
    String mode = "manual";
    String on_time = "12:00";
    String off_time = "13:00";
};

class PinController {
public:
    void setup(const int* pins, size_t length) {
        for (size_t i = 0; i < length; ++i) {
            int pin = pins[i];
            pinMode(pin, OUTPUT);
            digitalWrite(pin, LOW);
            pinMap[pin] = PinConfig();
        }
    }

    std::vector<int> handleAutoLogic() {
    std::vector<int> changedPins;
    int nowMinutes = hour() * 60 + minute();

    for (auto& [pin, cfg] : pinMap) {
        if (cfg.mode != "auto") continue;

        int onH, onM, offH, offM;
        sscanf(cfg.on_time.c_str(), "%d:%d", &onH, &onM);
        sscanf(cfg.off_time.c_str(), "%d:%d", &offH, &offM);

        int onMins = onH * 60 + onM;
        int offMins = offH * 60 + offM;

        bool isOn = (onMins < offMins)
                      ? (nowMinutes >= onMins && nowMinutes < offMins)
                      : (nowMinutes >= onMins || nowMinutes < offMins);

        int newState = isOn ? HIGH : LOW;

        if (digitalRead(pin) != newState) {
            digitalWrite(pin, newState);
            changedPins.push_back(pin); // 💡 Добавляем пин в список
            Serial.printf("Auto control: Pin %d set to %d\n", pin, newState);
        }
    }
    return changedPins;
}


    int handleCommand(const String& msg) {
    StaticJsonDocument<512> doc;
    DeserializationError err = deserializeJson(doc, msg);
    if (err) return -1;

    const char* action = doc["action"];
    if (!action) return -1;

    int pin = doc["pin"] | -1;

    if (strcmp(action, "set_state") == 0 && pin != -1) {
        int state = doc["state"];
        applyState(pin, state);
        return pin;
    }
    else if (strcmp(action, "set_mode") == 0 && pin != -1) {
        setMode(pin, doc["mode"] | "manual");
        return pin;
    }
    else if (strcmp(action, "set_schedule") == 0 && pin != -1) {
        setSchedule(pin, doc["schedule"]["on_time"] | "12:00", doc["schedule"]["off_time"] | "13:00");
        return pin;
    }
    else if (strcmp(action, "report") == 0) {
        return -1;  // → репорт на все
    }

    return -1;
}

    void applyState(int pin, int state) {
        if (pinMap.count(pin)) {
            pinMode(pin, OUTPUT);
            digitalWrite(pin, state);
            Serial.printf("Pin %d set to %d\n", pin, state);
        }
    }

    void setMode(int pin, const String& mode) {
        if (pinMap.count(pin)) {
            pinMap[pin].mode = mode;
            Serial.printf("Pin %d mode set to %s\n", pin, mode.c_str());
        }
    }

    void setSchedule(int pin, const String& on, const String& off) {
        if (pinMap.count(pin)) {
            pinMap[pin].on_time = on;
            pinMap[pin].off_time = off;
            Serial.printf("Pin %d schedule set %s - %s\n", pin, on.c_str(), off.c_str());
        }
    }


    String generateReport(int pin = -1) const {
        StaticJsonDocument<512> doc;
        doc["type"] = "report";
        JsonArray list = doc.createNestedArray("pin_list");

        if (pin == -1) {
            for (auto& [p, cfg] : pinMap) addToReport(list, p, cfg);
        } else if (pinMap.count(pin)) {
            addToReport(list, pin, pinMap.at(pin));
        }

        String result;
        serializeJson(doc, result);
        Serial.println(result);
        return result;
    }

private:
    std::map<int, PinConfig> pinMap;

    static void addToReport(JsonArray& arr, int pin, const PinConfig& cfg) {
        JsonObject obj = arr.createNestedObject();
        obj["pin"] = pin;
        obj["state"] = digitalRead(pin);
        obj["mode"] = cfg.mode;
        obj["schedule"]["on_time"] = cfg.on_time;
        obj["schedule"]["off_time"] = cfg.off_time;
    }
};