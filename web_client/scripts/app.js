// app.js
import { wsClient, wsSender } from "./websocket.js";
import { renderPins } from "./renderer.js";
import { changeDeviceStatus } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  const status = document.getElementById("connection_status");
  wsClient.onOpen = (ws) => {
    changeDeviceStatus(false);
    wsSender.authenticate("abc123");
    wsSender.get_report();
  };

  wsClient.onMessage = (event, ws) => {
    try {
      const data = JSON.parse(event.data);
      console.log("Received data:", data);
      if (data.type === "report") {
        renderPins(data, ws);
      } else if (data.type === "device_status") {
        changeDeviceStatus(data.status);
      }
    } catch (err) {
      console.error("Ошибка парсинга JSON:", err);
    }
  };

  // wsClient.onClose = () => {
  //
  // };
});
