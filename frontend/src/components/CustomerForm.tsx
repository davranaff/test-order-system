import React from 'react';
import { CustomerInfo } from '../services/api';

interface CustomerFormProps {
    customer: CustomerInfo;
    onChange: (customer: CustomerInfo) => void;
    className?: string;
}

export const CustomerForm: React.FC<CustomerFormProps> = ({ customer, onChange, className }) => {
    return (
        <div className={`customer-form ${className || ''}`}>
            <h3>Customer Information</h3>
            <div className="form-group">
                <label htmlFor="name">Name:</label>
                <input
                    type="text"
                    id="name"
                    value={customer.name}
                    onChange={(e) => onChange({ ...customer, name: e.target.value })}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="phone">Phone:</label>
                <input
                    type="tel"
                    id="phone"
                    value={customer.phone}
                    onChange={(e) => onChange({ ...customer, phone: e.target.value })}
                    pattern="\\+[0-9]{12}"
                    placeholder="+998901234567"
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    value={customer.email}
                    onChange={(e) => onChange({ ...customer, email: e.target.value })}
                    required
                />
            </div>
        </div>
    );
};
