import axios from 'axios';
import { Order, Product, OrderStatus } from '../types';

const API_URL = 'http://localhost:8000/api/v1';

export interface CustomerInfo {
    name: string;
    phone: string;
    email: string;
}

export interface OrderItemCreate {
    product_id: string;
    quantity: number;
    special_requests?: string;
}

export interface CreateOrderRequest {
    customer: CustomerInfo;
    items: OrderItemCreate[];
    notes?: string;
    delivery_address?: string;
    delivery_time?: string;
}

export interface ProductListResponse {
    products: Product[];
    total: number;
}

export interface OrderListResponse {
    orders: Order[];
    total: number;
}

export const api = {
    async getProducts(params: {
        category?: string;
        available_only?: boolean;
        page?: number;
        limit?: number;
    } = {}): Promise<ProductListResponse> {
        const response = await axios.get(`${API_URL}/products/`, { params });
        return response.data;
    },

    async getOrders(params: {
        status?: OrderStatus;
        page?: number;
        limit?: number;
    } = {}): Promise<OrderListResponse> {
        const response = await axios.get(`${API_URL}/orders/`, { params });
        return response.data;
    },

    async createOrder(orderData: CreateOrderRequest): Promise<Order> {
        const response = await axios.post(`${API_URL}/orders/`, orderData);
        return response.data;
    },

    async updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order> {
        const response = await axios.patch(`${API_URL}/orders/${orderId}/status`, { status });
        return response.data;
    },

    async cancelOrder(orderId: string): Promise<Order> {
        const response = await axios.patch(`${API_URL}/orders/${orderId}/status`, {
            status: OrderStatus.CANCELLED
        });
        return response.data;
    },

    async getOrderStats(): Promise<{ [key: string]: number }> {
        const response = await axios.get(`${API_URL}/orders/statistics/overview`);
        return response.data;
    }
};
