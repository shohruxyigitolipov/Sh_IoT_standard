// websocket.js
export class ReconnectingWebSocketWrapper {
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
