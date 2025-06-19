// webapp/app.js

const ws = new WebSocket("ws://localhost:8000/interfaces/web/ws/1/connect");

const log = document.getElementById("log");
const status = document.getElementById("connection_status");
const container = document.getElementById("pins_container");

ws.onopen = () => {
    status.innerText = "✅ Подключено к серверу";
    ws.send(JSON.stringify({auth_token: "abc123", client: "web"}))
    ws.send(JSON.stringify({action: "get_pins" }));
};

ws.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        console.log("Recieved data:", data)
        if (data.type === "pin_list") {
            renderPins(data.list);
        } else if (data.type === "log") {
            log.innerText = "Лог: " + data.message;
        } else if (data.action === "set_state") {
            const button = document.getElementById("GPIO"+data.pin)
            button.innerText = data.state ? "Выключить" : "Включить";
        }
    } catch (error) {
        console.error("Error parsing JSON:", error); // Логируем ошибку парсинга
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
        label.innerText = `Пин ${pin.pin}`;

        const button = document.createElement("button");
        button.innerText = pin.state ? "Выключить" : "Включить";
        button.className = "bg-blue-600 px-4 py-1 rounded hover:bg-blue-500";
        button.id = "GPIO"+pin.pin;
        button.onclick = () => {
            let state = button.innerText === "Включить" ? 1: 0;
            ws.send(JSON.stringify({
                action: "set_state",
                pin: pin.pin,
                state: state
            }));
        };


        div.appendChild(label);
        div.appendChild(button);
        container.appendChild(div);
    });
}
