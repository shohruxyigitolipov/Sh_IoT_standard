// WebSocketManager.h
#pragma once

#include <ArduinoWebsockets.h>
#include <functional>
#include "PinController.h"

using namespace websockets;

class WebSocketManager {
public:
    WebSocketManager(PinController& pinCtrl)
        : pinController(pinCtrl) {}

    void connect(const char* url, const String& token) {
        wsUrl = url;
        authToken = token;

        client.onEvent([this](WebsocketsEvent evt, String data) {
            switch (evt) {
                case WebsocketsEvent::ConnectionOpened:
                    connected = true;
                    Serial.println("WS connected");
                    client.send(authToken);
                    break;
                case WebsocketsEvent::ConnectionClosed:
                    connected = false;
                    Serial.println("WS disconnected");
                    break;
                default:
                    break;
            }
        });

        client.onMessage([this](WebsocketsMessage msg) {
            String data = msg.data();
            Serial.print("WS msg: ");
            Serial.println(data);

            if (data == "ping") {
                client.send("pong");
                return;
            }
            int result = pinController.handleCommand(data);
            if (result != -2) {
            client.send(pinController.generateReport());
}
        });

        if (client.connect(wsUrl)) {
            Serial.println("WS initial connection OK");
        } else {
            Serial.println("WS initial connection failed");
        }
    }

    void loop() {
        client.poll();
    }

    void send(const String& msg) {
        if (connected) client.send(msg);
    }

    bool isConnected() const {
        return connected;
    }

private:
    WebsocketsClient client;
    PinController& pinController;
    String authToken;
    const char* wsUrl;
    bool connected = false;
};
