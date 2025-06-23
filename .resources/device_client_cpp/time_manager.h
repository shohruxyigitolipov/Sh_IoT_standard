// TimeManager.h
#pragma once

#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

class TimeManager {
public:
    TimeManager(long gmtOffsetSec)
        : timeClient(ntpUDP, "pool.ntp.org", gmtOffsetSec, 60000) {}

    void begin() {
        timeClient.begin();
        sync();
    }

    void sync() {
        if (timeClient.update()) {
            setTime(timeClient.getEpochTime());
            Serial.print("Time synced: ");
            Serial.println(timeClient.getFormattedTime());
        }
    }

private:
    WiFiUDP ntpUDP;
    NTPClient timeClient;
};