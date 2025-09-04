import React, { useEffect, useState } from 'react';
import { Order, OrderStatus } from '../types';
import { OrderList } from '../components/OrderList';
import { api } from '../services/api';
import { wsService } from '../services/websocket';

export const OrdersPage: React.FC = () => {
    const [orders, setOrders] = useState<Order[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [statusFilter, setStatusFilter] = useState<OrderStatus | 'ALL'>('ALL');

    useEffect(() => {
        loadOrders();
        wsService.connect('staff');

        const unsubscribe = wsService.subscribe((data) => {
            console.log('Received WebSocket message:', data);

            if (data.type === 'error') {
                setError(data.error || 'An error occurred');
                setTimeout(() => setError(null), 5000);
            } else if (data.type === 'ORDER_UPDATED') {
                setOrders(prev =>
                    prev.map(order =>
                        order.id === data.order.id ? data.order : order
                    )
                );
            } else if (data.type === 'ORDER_CREATED') {
                setOrders(prev => [...prev, data.order]);
            }
        });

        return () => {
            unsubscribe();
            wsService.disconnect();
        };
    }, []);

    const loadOrders = async () => {
        try {
            const data = await api.getOrders();
            setOrders(data.orders);
        } catch (err) {
            setError('Failed to load orders');
        }
    };

    const handleStatusUpdate = async (orderId: string, status: OrderStatus) => {
        try {
            const updatedOrder = await api.updateOrderStatus(orderId, status);
            setOrders(prev =>
                prev.map(order =>
                    order.id === updatedOrder.id ? updatedOrder : order
                )
            );
        } catch (err) {
            setError('Failed to update order status');
        }
    };

    const handleCancel = async (orderId: string) => {
        try {
            const cancelledOrder = await api.cancelOrder(orderId);
            setOrders(prev =>
                prev.map(order =>
                    order.id === cancelledOrder.id ? cancelledOrder : order
                )
            );
        } catch (err) {
            setError('Failed to cancel order');
        }
    };

    const filteredOrders = orders.filter(order =>
        statusFilter === 'ALL' || order.status === statusFilter
    );

    return (
        <div className="orders-page">

            <div className="orders-section">
                <div className="filters">
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value as OrderStatus | 'ALL')}
                    >
                        <option value="ALL">All Orders</option>
                        {Object.values(OrderStatus).map(status => (
                            <option key={status} value={status}>
                                {status}
                            </option>
                        ))}
                    </select>
                </div>

                {error && <div className="error-message">{error}</div>}

                <OrderList
                    orders={filteredOrders}
                    onStatusUpdate={handleStatusUpdate}
                    onCancel={handleCancel}
                />
            </div>
        </div>
    );
};
