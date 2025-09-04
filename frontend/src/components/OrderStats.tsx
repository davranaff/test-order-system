import React from 'react';
import { OrderStats as OrderStatsType } from '../types';

interface OrderStatsProps {
    stats: OrderStatsType;
}

export const OrderStats: React.FC<OrderStatsProps> = ({ stats }) => {
    return (
        <div className="order-stats">
            <h2>Order Statistics</h2>
            <div className="stats-grid">
                {Object.entries(stats).map(([status, count]) => (
                    <div key={status} className={`stat-card status-${status.toLowerCase()}`}>
                        <h3>{status}</h3>
                        <p className="stat-count">{count}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};
