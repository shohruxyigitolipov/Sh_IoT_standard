import {wsSender} from "./websocket.js";

export function changeDeviceStatus(status, render) {
    const deviceStatus = document.getElementById("device_status");
    if (!deviceStatus) return;

    if (status) {
        deviceStatus.classList.remove("offline");
        deviceStatus.classList.add("online");
        if (render) {
            wsSender.get_report();
        }
    } else {
        deviceStatus.classList.remove("online");
        deviceStatus.classList.add("offline");
    }
}
