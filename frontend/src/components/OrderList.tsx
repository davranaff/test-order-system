import React from 'react';
import { Order, OrderStatus } from '../types';

interface OrderListProps {
    orders: Order[];
    onStatusUpdate: (orderId: string, status: OrderStatus) => void;
    onCancel: (orderId: string) => void;
}

const getNextStatuses = (currentStatus: OrderStatus): OrderStatus[] => {
    switch (currentStatus) {
        case OrderStatus.NEW:
            return [OrderStatus.CONFIRMED, OrderStatus.CANCELLED];
        case OrderStatus.CONFIRMED:
            return [OrderStatus.PREPARING, OrderStatus.CANCELLED];
        case OrderStatus.PREPARING:
            return [OrderStatus.READY, OrderStatus.CANCELLED];
        case OrderStatus.READY:
            return [OrderStatus.COMPLETED, OrderStatus.CANCELLED];
        case OrderStatus.COMPLETED:
            return [];
        case OrderStatus.CANCELLED:
            return [];
        default:
            return [];
    }
};

export const OrderList: React.FC<OrderListProps> = ({ orders, onStatusUpdate, onCancel }) => {
    return (
        <div className="order-list">
            <h2>Orders</h2>
            <div className="orders-container">
                {orders.map(order => {
                    const availableStatuses = getNextStatuses(order.status);

                    return (
                        <div key={order.id} className={`order-card status-${order.status.toLowerCase()}`}>
                            <div className="order-header">
                                <h3>Order #{order.id}</h3>
                                <span className="order-date">
                                    {new Date(order.created_at).toLocaleDateString()}
                                </span>
                            </div>
                            <div className="order-items">
                                {order.items.map(item => (
                                    <div key={item.id} className="order-item">
                                        <span>{item.name}</span>
                                        <span>x{item.quantity}</span>
                                        <span>${item.price}</span>
                                    </div>
                                ))}
                            </div>
                            <div className="order-footer">
                                <div className="order-total">
                                    Total: ${order.total}
                                </div>
                                <div className="order-actions">
                                    {availableStatuses.length > 0 && (
                                        <select
                                            value={order.status}
                                            onChange={(e) => onStatusUpdate(order.id, e.target.value as OrderStatus)}
                                        >
                                            <option value={order.status}>{order.status}</option>
                                            {availableStatuses.map(status => (
                                                <option key={status} value={status}>
                                                    {status}
                                                </option>
                                            ))}
                                        </select>
                                    )}
                                    {order.status !== OrderStatus.CANCELLED && (
                                        <button
                                            className="cancel-button"
                                            onClick={() => onCancel(order.id)}
                                        >
                                            Cancel Order
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
