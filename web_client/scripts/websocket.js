// websocket.js
export class WebSocketWrapper {
  constructor(url, protocols = []) {
    this.url = url;
    this.protocols = protocols;
    this.reconnectInterval = 3000;
    this.maxRetries = 10;
    this.retryCount = 0;
    this.init();
  }

  init() {
    this.ws = new WebSocket(this.url, this.protocols);

    this.ws.onopen = () => {
      this.onOpen && this.onOpen(this.ws);
      this.retryCount = 0;
    };

    this.ws.onmessage = (event) => {
      this.onMessage && this.onMessage(event, this.ws);
    };

    this.ws.onclose = (event) => {
      this.onClose && this.onClose(event);
      this.reconnect();
    };

    this.ws.onerror = () => {
      this.ws.close();
    };
  }

  reconnect() {
    if (this.retryCount < this.maxRetries) {
      setTimeout(() => {
        this.retryCount++;
        console.log(`🔁 Попытка переподключения #${this.retryCount}`);
        this.init();
      }, this.reconnectInterval);
    } else {
      console.error("❌ Не удалось переподключиться к WebSocket.");
    }
  }
}

export class WebSocketSender {
  constructor(ws) {
    this.ws = ws;
  }

  authenticate(auth_token) {
    this._send({
      auth_token: auth_token
    })
  }

  get_report() {
    this._send({
      action: 'get_report'
    })
  }

  set_mode(pin, mode) {
    this._send({
      action: "set_mode",
      pin: pin,
      mode: mode
    })
  }

  set_state(pin, state) {
    this._send({
      action: "set_state",
      pin: pin,
      state: state
    })
  }

  set_schedule(pin, on_time, off_time) {
      this._send({
          action: "set_schedule",
          pin: pin,
          schedule: {
              on_time: on_time,
              off_time: off_time
          }
      })
  }

  _send(data) {
    this.ws.send(JSON.stringify(data))
    console.log('hello')
  }
}

export const wsClient = new WebSocketWrapper("ws://localhost:8000/interfaces/web/ws/1/connect");
export const wsSender = new WebSocketSender(wsClient.ws);