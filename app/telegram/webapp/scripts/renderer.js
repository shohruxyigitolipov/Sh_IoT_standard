import { createModeSelect, createToggle, createTimeRow } from "./components.js";
import { changeDeviceStatus } from "./utils.js";

export function renderPin(pin, ws) {
  const container = document.getElementById("pins_container");
  const newDiv = document.createElement("div");
  newDiv.className = "flex flex-col gap-2 bg-gray-700 p-3 rounded";
  newDiv.id = `pin-wrapper-${pin.pin}`;

  const topRow = document.createElement("div");
  topRow.className = "flex justify-between items-center gap-2";

  const leftGroup = document.createElement("div");
  leftGroup.className = "flex items-center gap-4";

  const label = document.createElement("span");
  label.innerText = `GPIO${pin.pin}`;
  const modeSelect = createModeSelect(pin, ws);

  leftGroup.append(label, modeSelect);
  topRow.appendChild(leftGroup);

  if (["manual", "auto"].includes(pin.mode)) {
    const toggle = createToggle(pin, ws);
    topRow.appendChild(toggle);
  }

  newDiv.appendChild(topRow);

  if (pin.mode === "auto") {
    const timeRow = createTimeRow(pin, ws);
    newDiv.appendChild(timeRow);
  }

  const existing = document.getElementById(newDiv.id);
  if (existing) {
    container.replaceChild(newDiv, existing);
  } else {
    container.appendChild(newDiv);
  }
}

export function renderPins(data, ws) {
  data.pin_list.forEach(pin => renderPin(pin, ws));
  changeDeviceStatus(true);
}