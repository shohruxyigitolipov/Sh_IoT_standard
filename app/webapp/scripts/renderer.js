
// renderer.js

export function renderPin(pin, ws) {
  const container = document.getElementById("pins_container");
  const newDiv = document.createElement("div");
  newDiv.className = "flex flex-col gap-2 bg-gray-700 p-3 rounded";
  newDiv.id = "pin-wrapper-" + pin.pin;

  const topRow = document.createElement("div");
  topRow.className = "flex justify-between items-center gap-2";

  const leftGroup = document.createElement("div");
  leftGroup.className = "flex items-center gap-4";

  const label = document.createElement("span");
  label.innerText = `GPIO${pin.pin}`;

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
    const newMode = modeSelect.value;
    ws.send(JSON.stringify({
      action: "set_mode",
      pin: pin.pin,
      mode: newMode
    }));
    pin.mode = newMode;
    renderPin(pin, ws);
  };

  leftGroup.append(label, modeSelect);
  topRow.appendChild(leftGroup);

  
  if (pin.mode === "manual") {
    const button = document.createElement("button");
    button.innerText = pin.state ? "ВЫКЛ" : "ВКЛ";
    button.title = "Переключить состояние пина вручную";
    button.className = (pin.state
      ? "bg-red-600 hover:bg-red-500"
      : "bg-green-600 hover:bg-green-500") + " px-4 py-1 rounded transition-colors";
    button.id = "GPIO" + pin.pin;
    button.onclick = () => {
      const state = button.innerText === "ВКЛ" ? 1 : 0;
      ws.send(JSON.stringify({
        action: "set_state",
        pin: pin.pin,
        state
      }));
    };
    topRow.appendChild(button);
  }

  newDiv.appendChild(topRow);

  
  if (pin.mode === "auto") {
    const timeRow = document.createElement("div");
    timeRow.className = "flex justify-end items-center mt-2 gap-2 text-sm text-white";

    const fromInput = document.createElement("input");
    fromInput.type = "time";
    fromInput.title = "Время включения";
    fromInput.className = "bg-gray-800 text-white p-1 rounded w-[100px]";
    fromInput.value = pin.schedule?.on_time || "";

    const separator = document.createElement("span");
    separator.innerText = "–";

    const toInput = document.createElement("input");
    toInput.type = "time";
    toInput.title = "Время выключения";
    toInput.className = "bg-gray-800 text-white p-1 rounded w-[100px]";
    toInput.value = pin.schedule?.off_time || "";

    const sendSchedule = () => {
      if (fromInput.value && toInput.value) {
        ws.send(JSON.stringify({
          action: "set_schedule",
          pin: pin.pin,
          schedule:{
            on_time: fromInput.value,
            off_time: toInput.value
          }
        }));
      }
    };

    fromInput.onchange = sendSchedule;
    toInput.onchange = sendSchedule;

    timeRow.append(fromInput, separator, toInput);
    newDiv.appendChild(timeRow);
  }

  const existing = document.getElementById(newDiv.id);
  if (existing) {
    container.replaceChild(newDiv, existing); // сохраняет позицию
  } else {
    container.appendChild(newDiv); // новый — в конец
  }
}

export function renderReport(data, ws) {
  if (data.pin_list.length > 1) {
    data.pin_list.forEach(pin => renderPin(pin, ws));
  } else {
    renderPin(data.pin_list[0], ws)
  }
}
