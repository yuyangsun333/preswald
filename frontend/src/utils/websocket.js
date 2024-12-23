class WebSocketClient {
    constructor() {
        this.callbacks = new Set();
        this.socket = null;
        this.clientId = Math.random().toString(36).substring(7);
        this.isConnecting = false;
        console.log("WebSocketClient initialized with ID:", this.clientId);
    }

    connect() {
        if (this.isConnecting) return;
        this.isConnecting = true;

        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/${this.clientId}`;
        console.log("Connecting to WebSocket:", wsUrl);

        try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                console.log("WebSocket connection established");
                this.isConnecting = false;
            };

            this.socket.onmessage = (event) => {
                try {
                    console.log("WebSocket message received:", event.data);
                    const data = JSON.parse(event.data);
                    this.callbacks.forEach(callback => callback(data));
                } catch (error) {
                    console.error("Error processing WebSocket message:", error);
                }
            };

            this.socket.onclose = () => {
                console.log("WebSocket connection closed, attempting reconnect...");
                this.isConnecting = false;
                setTimeout(() => this.connect(), 1000);
            };

            this.socket.onerror = (error) => {
                console.error("WebSocket error:", error);
                this.isConnecting = false;
            };
        } catch (error) {
            console.error("Error creating WebSocket:", error);
            this.isConnecting = false;
            setTimeout(() => this.connect(), 1000);
        }
    }

    subscribe(callback) {
        console.log("New subscriber added");
        this.callbacks.add(callback);
        return () => {
            console.log("Subscriber removed");
            this.callbacks.delete(callback);
        };
    }

    sendMessage(message) {
        if (this.socket?.readyState === WebSocket.OPEN) {
            console.log("Sending WebSocket message:", message);
            this.socket.send(JSON.stringify(message));
        } else {
            console.warn("Cannot send message, WebSocket not open");
        }
    }
}

export const websocket = new WebSocketClient(); 