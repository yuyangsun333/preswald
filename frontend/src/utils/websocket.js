class WebSocketClient {
    constructor() {
        this.callbacks = new Set();
        this.socket = null;
        this.clientId = Math.random().toString(36).substring(7);
        this.isConnecting = false;
        this.componentStates = {};
        console.log("[WebSocket] Initialized with ID:", this.clientId);
    }

    connect() {
        if (this.isConnecting) return;
        this.isConnecting = true;

        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/${this.clientId}`;
        console.log("[WebSocket] Connecting to:", wsUrl);

        try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                console.log("[WebSocket] Connection established");
                this.isConnecting = false;
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
                    
                    this.callbacks.forEach(callback => callback(data));
                } catch (error) {
                    console.error("[WebSocket] Error processing message:", error);
                }
            };

            this.socket.onclose = () => {
                console.log("[WebSocket] Connection closed, attempting reconnect...");
                this.isConnecting = false;
                setTimeout(() => this.connect(), 1000);
            };

            this.socket.onerror = (error) => {
                console.error("[WebSocket] Error:", error);
                this.isConnecting = false;
            };
        } catch (error) {
            console.error("[WebSocket] Error creating connection:", error);
            this.isConnecting = false;
            setTimeout(() => this.connect(), 1000);
        }
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
            return;
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