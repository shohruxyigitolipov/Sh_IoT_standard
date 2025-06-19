// app.js
import { ReconnectingWebSocketWrapper } from "./websocket.js";
import { renderReport } from "./renderer.js";

document.addEventListener("DOMContentLoaded", () => {
  const log = document.getElementById("log");
  const status = document.getElementById("connection_status");

  const wsClient = new ReconnectingWebSocketWrapper("wss://shiotstandard-production.up.railway.app/interfaces/web/ws/1/connect");

  wsClient.onOpen = (ws) => {
    status.innerText = "✅ Подключено к серверу";
    ws.send(JSON.stringify({ auth_token: "abc123", client: "web" }));
    ws.send(JSON.stringify({ action: "get_report" }));
    console.log("Я родился")
  };

  wsClient.onMessage = (event, ws) => {
    try {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);

      if (data.type === "report") {
        renderReport(data, ws);
      } else if (data.type === "log") {
        log.innerText = "Лог: " + data.message;
      } else if (data.action === "set_state") {
        const btn = document.getElementById("GPIO" + data.pin);
        btn.innerText = data.state ? "Выключить" : "Включить";
      }
    } catch (err) {
      console.error("Ошибка парсинга JSON:", err);
    }
  };

  wsClient.onClose = (event) => {
    status.innerText = "❌ Соединение закрыто. Переподключение...";
  };
});
