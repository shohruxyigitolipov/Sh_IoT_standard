// app.js
import { WebSocketWrapper } from "./websocket.js";
import { renderPins } from "./renderer.js";
import { changeDeviceStatus } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const status = document.getElementById("connection_status");
  const wsClient = new WebSocketWrapper("ws://localhost:8000/interfaces/web/ws/1/connect");

  wsClient.onOpen = (ws) => {
    status.innerText = "✅ Подключено к серверу";
    changeDeviceStatus(false);
    ws.send(JSON.stringify({ auth_token: "abc123", client: "web" }));
    ws.send(JSON.stringify({ action: "get_report" }));
  };

  wsClient.onMessage = (event, ws) => {
    try {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);

      if (data.type === "report") {
        renderPins(data, ws);
      } else if (data.type === "device_status") {
        changeDeviceStatus(data.status, ws);
      }
    } catch (err) {
      console.error("Ошибка парсинга JSON:", err);
    }
  };

  wsClient.onClose = () => {
    status.innerText = "❌ Соединение закрыто. Переподключение...";
  };
});
