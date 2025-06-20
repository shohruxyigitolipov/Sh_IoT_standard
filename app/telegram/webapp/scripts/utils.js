import {wsSender} from "./websocket.js";

export function changeDeviceStatus(status, render) {
    const deviceStatus = document.getElementById("device_status");
    if (status) {
        deviceStatus.innerText = "Устройство активно";
        if (render) {
            wsSender.get_report();
        }
    } else {
        deviceStatus.innerText = "Устройство не активно";

        const container = document.getElementById("pins_container");
        container.innerHTML = '';
    }
}
