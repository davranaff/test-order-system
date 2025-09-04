export interface WebSocketMessage {
    type: string;
    order?: any;
    stats?: {
        [key: string]: number;
    };
    error?: string;
}

type MessageHandler = (data: WebSocketMessage) => void;

export class WebSocketService {
    private ws: WebSocket | null = null;
    private messageHandlers: Set<MessageHandler> = new Set();
    private reconnectAttempts: number = 0;
    private maxReconnectAttempts: number = 5;
    private reconnectTimeout: number | null = null;
    private currentRole: string = 'customers';

    connect(role: string = 'customers') {
        this.currentRole = role;
        this.createConnection();
    }

    private createConnection() {
        try {
            if (this.ws?.readyState === WebSocket.OPEN) {
                console.log('WebSocket is already connected');
                return;
            }

            this.ws = new WebSocket(`ws://localhost:8000/ws/${this.currentRole}`);
            this.setupWebSocketHandlers();
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            this.handleReconnect();
        }
    }

    private setupWebSocketHandlers() {
        if (!this.ws) return;

        this.ws.onopen = this.handleOpen.bind(this);
        this.ws.onmessage = this.handleMessage.bind(this);
        this.ws.onclose = this.handleClose.bind(this);
        this.ws.onerror = this.handleError.bind(this);
    }

    private handleOpen(event: Event) {
        console.log('WebSocket connected successfully');
        this.reconnectAttempts = 0;
    }

    private handleMessage(event: MessageEvent) {
        try {
            const data: WebSocketMessage = JSON.parse(event.data);
            console.log('Received WebSocket message:', data);
            this.messageHandlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error('Error in message handler:', error);
                }
            });
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    }

    private handleClose(event: CloseEvent) {
        console.log(`WebSocket connection closed: ${event.code} ${event.reason}`);

        if (event.code !== 1000) {
            this.handleReconnect();
        }
    }

    private handleError(event: Event) {
        console.error('WebSocket error:', event);
    }

    private handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            return;
        }

        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        this.reconnectAttempts++;

        console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

        if (this.reconnectTimeout) {
            window.clearTimeout(this.reconnectTimeout);
        }

        this.reconnectTimeout = window.setTimeout(() => {
            console.log('Attempting to reconnect...');
            this.createConnection();
        }, delay);
    }

    subscribe(handler: MessageHandler): () => void {
        this.messageHandlers.add(handler);
        return () => {
            this.messageHandlers.delete(handler);
        };
    }

    disconnect() {
        if (this.reconnectTimeout) {
            window.clearTimeout(this.reconnectTimeout);
            this.reconnectTimeout = null;
        }

        if (this.ws) {
            try {
                this.ws.close(1000, 'Client disconnecting normally');
            } catch (error) {
                console.error('Error closing WebSocket:', error);
            } finally {
                this.ws = null;
                this.reconnectAttempts = 0;
                this.messageHandlers.clear();
            }
        }
    }
}

export const wsService = new WebSocketService();
