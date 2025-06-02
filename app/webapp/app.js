// webapp/app.js

const ws = new WebSocket("ws://localhost:8000/devices/ws/1/connect");  // временно user_id = 123

const log = document.getElementById("log");
const status = document.getElementById("connection_status");
const container = document.getElementById("pins_container");

ws.onopen = () => {
    status.innerText = "✅ Подключено к серверу";
    ws.send(JSON.stringify({auth_token: "abc123", client: "web"}))
    ws.send(JSON.stringify({ action: "get_pins" }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "pin_list") {
        renderPins(data.pins);
    } else if (data.type === "log") {
        log.innerText = "Лог: " + data.message;
    }
};

ws.onclose = () => {
    status.innerText = "❌ Соединение закрыто";
};

function renderPins(pins) {
    container.innerHTML = '';
    pins.forEach(pin => {
        const div = document.createElement("div");
        div.className = "flex items-center justify-between bg-gray-700 p-3 rounded";

        const label = document.createElement("span");
        label.innerText = `Пин ${pin.id}`;

        const button = document.createElement("button");
        button.innerText = pin.state ? "Выключить" : "Включить";
        button.className = "bg-blue-600 px-4 py-1 rounded hover:bg-blue-500";
        button.onclick = () => {
            ws.send(JSON.stringify({
                action: "toggle_pin",
                pin_id: pin.id
            }));
        };

        div.appendChild(label);
        div.appendChild(button);
        container.appendChild(div);
    });
}
