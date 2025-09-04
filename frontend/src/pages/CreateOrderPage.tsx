import React, { useEffect, useState } from 'react';
import { Product } from '../types';
import { ProductList } from '../components/ProductList';
import { api, CustomerInfo } from '../services/api';
import { CustomerForm } from '../components/CustomerForm';

interface CartItem {
    product: Product;
    quantity: number;
}

export const CreateOrderPage: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [cartItems, setCartItems] = useState<CartItem[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [customer, setCustomer] = useState<CustomerInfo>({
        name: '',
        phone: '',
        email: ''
    });

    useEffect(() => {
        loadProducts();
    }, []);

    const loadProducts = async () => {
        try {
            const data = await api.getProducts({ available_only: true });
            setProducts(data.products);
        } catch (err) {
            setError('Failed to load products');
        }
    };

    const handleAddToCart = (product: Product, quantity: number) => {
        setCartItems(prev => {
            const existingItem = prev.find(item => item.product.id === product.id);
            if (existingItem) {
                return prev.map(item =>
                    item.product.id === product.id
                        ? { ...item, quantity: item.quantity + quantity }
                        : item
                );
            }
            return [...prev, { product, quantity }];
        });
    };

    const handleCreateOrder = async () => {
        if (cartItems.length === 0) return;

        setIsLoading(true);
        setError(null);

        try {
            const orderData = {
                customer,
                items: cartItems.map(item => ({
                    product_id: item.product.id,
                    quantity: item.quantity
                }))
            };

            await api.createOrder(orderData);
            setCartItems([]);
        } catch (err) {
            setError('Failed to create order');
        } finally {
            setIsLoading(false);
        }
    };

    const cartTotal = cartItems.reduce(
        (total, item) => total + item.product.price * item.quantity,
        0
    );

    return (
        <div className="create-order-page">
            <div className="main-content">
                <ProductList products={products} onAddToCart={handleAddToCart} />
            </div>

            <div className="cart-sidebar">
                <CustomerForm
                    customer={customer}
                    onChange={setCustomer}
                    className="cart-customer-form"
                />

                <h2>Cart</h2>
                {cartItems.length === 0 ? (
                    <p>Your cart is empty</p>
                ) : (
                    <>
                        {cartItems.map(item => (
                            <div key={item.product.id} className="cart-item">
                                <span>{item.product.name}</span>
                                <span>x{item.quantity}</span>
                                <span>${(item.product.price * item.quantity).toFixed(2)}</span>
                            </div>
                        ))}
                        <div className="cart-total">
                            <strong>Total: ${cartTotal.toFixed(2)}</strong>
                        </div>
                        <button
                            className="create-order-button"
                            onClick={handleCreateOrder}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Creating...' : 'Create Order'}
                        </button>
                        {error && <div className="error-message">{error}</div>}
                    </>
                )}
            </div>
        </div>
    );
};
