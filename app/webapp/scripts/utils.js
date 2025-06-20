export function changeDeviceStatus(status, ws) {
    const deviceStatus = document.getElementById("device_status");
    if (status) {
        deviceStatus.innerText = "Статус девайса: Активен";
        if (ws) {
            ws.send(JSON.stringify({ action: "get_report" }));
        }
    } else {
        const container = document.getElementById("pins_container");
        container.innerHTML = '';
        deviceStatus.innerText = "Статус девайса: Не активен"
    }
}
