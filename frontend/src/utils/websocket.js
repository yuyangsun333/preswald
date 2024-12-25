class WebSocketClient {
    constructor() {
        this.callbacks = new Set();
        this.socket = null;
        this.clientId = Math.random().toString(36).substring(7);
        this.isConnecting = false;
        this.componentStates = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
        console.log("[WebSocket] Initialized with ID:", this.clientId);
    }

    connect() {
        if (this.isConnecting || (this.socket && this.socket.readyState === WebSocket.OPEN)) {
            console.log("[WebSocket] Already connected or connecting");
            return;
        }

        this.isConnecting = true;
        console.log("[WebSocket] Connecting...");

        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/${this.clientId}`;
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                console.log("[WebSocket] Connected successfully");
                this.isConnecting = false;
                this.reconnectAttempts = 0;
                this.reconnectDelay = 1000;
                this._notifySubscribers({
                    type: "connection_status",
                    connected: true
                });
            };

            this.socket.onclose = (event) => {
                console.log("[WebSocket] Connection closed:", event);
                this.isConnecting = false;
                this._notifySubscribers({
                    type: "connection_status",
                    connected: false
                });
                this._handleReconnect();
            };

            this.socket.onerror = (error) => {
                console.error("[WebSocket] Error:", error);
                this.isConnecting = false;
                this._notifySubscribers({
                    type: "error",
                    content: {
                        message: "WebSocket connection error"
                    }
                });
            };

            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log("[WebSocket] Message received:", {
                        type: data.type,
                        data: data,
                        timestamp: new Date().toISOString()
                    });
                    
                    if (data.type === 'initial_state' && data.states) {
                        this.componentStates = { ...data.states };
                        console.log("[WebSocket] Initial states loaded:", this.componentStates);
                    }
                    else if (data.type === 'component_update' && data.component_id && 'value' in data) {
                        this.componentStates[data.component_id] = data.value;
                        console.log("[WebSocket] Component state updated from server:", {
                            componentId: data.component_id,
                            value: data.value,
                            allStates: this.componentStates
                        });
                    }
                    else if (data.type === 'components') {
                        // Update local states from component values
                        data.components.forEach(component => {
                            if (component.id && 'value' in component) {
                                this.componentStates[component.id] = component.value;
                                console.log("[WebSocket] Component state synced:", {
                                    componentId: component.id,
                                    value: component.value
                                });
                            }
                        });
                    }

                    // Notify subscribers
                    this._notifySubscribers(data);
                } catch (error) {
                    console.error("[WebSocket] Error processing message:", error);
                    this._notifySubscribers({
                        type: "error",
                        content: {
                            message: "Error processing server message"
                        }
                    });
                }
            };
        } catch (error) {
            console.error("[WebSocket] Error creating connection:", error);
            this.isConnecting = false;
            this._notifySubscribers({
                type: "error",
                content: {
                    message: "Failed to create WebSocket connection"
                }
            });
        }
    }

    disconnect() {
        if (this.socket) {
            console.log("[WebSocket] Disconnecting...");
            this.socket.close();
            this.socket = null;
        }
    }

    _handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log("[WebSocket] Max reconnection attempts reached");
            this._notifySubscribers({
                type: "error",
                content: {
                    message: "Failed to reconnect to server after multiple attempts"
                }
            });
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1), 30000);
        console.log(`[WebSocket] Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
                console.log("[WebSocket] Attempting reconnection...");
                this.connect();
            }
        }, delay);
    }

    _notifySubscribers(message) {
        this.callbacks.forEach(callback => {
            try {
                callback(message);
            } catch (error) {
                console.error("[WebSocket] Error in subscriber callback:", error);
            }
        });
    }

    subscribe(callback) {
        console.log("[WebSocket] New subscriber added");
        this.callbacks.add(callback);
        return () => {
            console.log("[WebSocket] Subscriber removed");
            this.callbacks.delete(callback);
        };
    }

    updateComponentState(componentId, value) {
        if (!componentId) {
            console.error("[WebSocket] Cannot update component state: missing componentId");
            return;
        }

        console.log("[WebSocket] Updating component state:", {
            componentId,
            oldValue: this.componentStates[componentId],
            newValue: value,
            timestamp: new Date().toISOString()
        });

        // Update local state immediately
        this.componentStates[componentId] = value;
        
        // Send update to server
        const message = {
            type: "component_update",
            states: {
                [componentId]: value
            }
        };

        this.sendMessage(message);
        console.log("[WebSocket] State update message sent:", {
            type: message.type,
            states: message.states
        });
    }

    sendMessage(message) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            console.warn("[WebSocket] Cannot send message, connection not open");
            throw new Error("WebSocket connection not open");
        }

        try {
            const messageStr = JSON.stringify(message);
            console.log("[WebSocket] Sending message:", {
                message,
                timestamp: new Date().toISOString()
            });
            this.socket.send(messageStr);
        } catch (error) {
            console.error("[WebSocket] Error sending message:", error);
            throw error;
        }
    }

    getComponentState(componentId) {
        const state = this.componentStates[componentId];
        console.log("[WebSocket] Getting component state:", {
            componentId,
            value: state
        });
        return state;
    }
}

export const websocket = new WebSocketClient(); 