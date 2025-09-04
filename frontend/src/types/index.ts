export enum OrderStatus {
    NEW = "новый",
    CONFIRMED = "подтвержден",
    PREPARING = "готовится",
    READY = "готов",
    COMPLETED = "выполнен",
    CANCELLED = "отменен",

}

export interface Product {
    id: string;
    name: string;
    price: number;
    category: string;
    description?: string;
    is_available: boolean;
}

export interface OrderItem {
    id: string;
    name: string;
    quantity: number;
    price: number;
    special_requests?: string;
}

export interface Customer {
    name: string;
    phone: string;
    email: string;
}

export interface Order {
    id: string;
    customer: Customer;
    items: OrderItem[];
    status: OrderStatus;
    total: number;
    created_at: string;
    notes?: string;
    delivery_address?: string;
    delivery_time?: string;
}

export interface OrderStats {
    [OrderStatus.NEW]: number;
    [OrderStatus.CONFIRMED]: number;
    [OrderStatus.PREPARING]: number;
    [OrderStatus.READY]: number;
    [OrderStatus.COMPLETED]: number;
    [OrderStatus.CANCELLED]: number;
}
