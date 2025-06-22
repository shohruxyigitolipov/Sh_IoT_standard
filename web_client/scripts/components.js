import {wsSender} from "./websocket.js";

export function createModeSelect(pin, ws) {
  const modeSelect = document.createElement("select");
  modeSelect.className = "bg-gray-800 text-white p-1 rounded";

  ["manual", "auto"].forEach(mode => {
    const option = document.createElement("option");
    option.value = mode;
    option.text = mode === "manual" ? "Ручной" : "Авто";
    if (pin.mode === mode) option.selected = true;
    modeSelect.appendChild(option);
  });

  modeSelect.onchange = () => {
    wsSender.set_mode(pin.pin, modeSelect.value);
  };

  return modeSelect;
}

export function createToggle(pin, ws) {
  const toggleWrapper = document.createElement("label");
  toggleWrapper.className = "relative inline-flex items-center cursor-pointer";

  const input = document.createElement("input");
  input.type = "checkbox";
  input.checked = !!pin.state;
  input.className = "sr-only peer";

  const toggleDiv = document.createElement("div");
  toggleDiv.className = "w-11 h-6 rounded-full peer bg-red-600 peer-checked:bg-green-600 peer-focus:ring-4 transition-all";
  toggleDiv.classList.add(
    "after:content-['']", "after:absolute", "after:top-[2px]", "after:left-[2px]",
    "after:bg-white", "after:border", "after:rounded-full",
    "after:h-5", "after:w-5", "after:transition-all",
    "peer-checked:after:translate-x-full", "peer-checked:after:border-white"
  );

  if (pin.mode === "auto") {
    input.disabled = true;
    toggleDiv.classList.add("opacity-50", "pointer-events-none");
  }

  input.onchange = () => {
    if (pin.mode === "manual") wsSender.set_state(pin.pin, input.checked ? 1 : 0);
  };

  toggleWrapper.append(input, toggleDiv);
  return toggleWrapper;
}

export function createTimeRow(pin, ws) {
  const timeRow = document.createElement("div");
  timeRow.className = "flex justify-center items-center mt-2 gap-2 text-sm text-white";

  const fromInput = document.createElement("input");
  fromInput.type = "time";
  fromInput.title = "Время включения";
  fromInput.className = "bg-gray-800 text-white p-1 rounded w-[100px]";
  fromInput.value = pin.schedule?.on_time || "";

  const toInput = document.createElement("input");
  toInput.type = "time";
  toInput.title = "Время выключения";
  toInput.className = "bg-gray-800 text-white p-1 rounded w-[100px]";
  toInput.value = pin.schedule?.off_time || "";

  const sendSchedule = () => {
    if (fromInput.value && toInput.value) {
      wsSender.set_schedule(pin.pin, fromInput.value, toInput.value);
    }
  };

  fromInput.onchange = sendSchedule;
  toInput.onchange = sendSchedule;

  timeRow.append(fromInput, document.createTextNode("–"), toInput);
  return timeRow;
}

export function createNameInput(pin) {
  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = `GPIO${pin.pin}`;
  input.className = "bg-gray-800 text-white p-1 rounded w-[120px] text-sm";
  input.value = pin.name || "";

  const send = () => {
    wsSender.set_pin_name(pin.pin, input.value);
  };

  input.addEventListener("blur", send);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      input.blur();
    }
  });
  return input;
}
