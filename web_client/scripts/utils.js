import {wsSender} from "./websocket.js";

export function changeDeviceStatus(status) {
    const deviceStatus = document.getElementById("device_status");
    if (!deviceStatus) return;

    if (status) {
        deviceStatus.classList.remove("offline");
        deviceStatus.classList.add("online");
    } else {
        deviceStatus.classList.remove("online");
        deviceStatus.classList.add("offline");
    }
}
