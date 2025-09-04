import React, { useState } from 'react';
import { Product } from '../types';

interface ProductListProps {
    products: Product[];
    onAddToCart: (product: Product, quantity: number) => void;
}

export const ProductList: React.FC<ProductListProps> = ({ products, onAddToCart }) => {
    const [quantities, setQuantities] = useState<{ [key: string]: number }>({});

    const handleQuantityChange = (productId: string, value: string) => {
        const quantity = parseInt(value) || 0;
        setQuantities(prev => ({
            ...prev,
            [productId]: quantity
        }));
    };

    return (
        <div className="product-list">
            <h2>Products</h2>
            <div className="products-grid">
                {products.map(product => (
                    <div key={product.id} className="product-card">
                        <h3>{product.name}</h3>
                        <p>{product.description}</p>
                        <p className="price">${product.price.toFixed(2)}</p>
                        <div className="product-actions">
                            <input
                                type="number"
                                min="1"
                                value={quantities[product.id] || ''}
                                onChange={(e) => handleQuantityChange(product.id, e.target.value)}
                                placeholder="Qty"
                            />
                            <button
                                onClick={() => onAddToCart(product, quantities[product.id] || 1)}
                                disabled={!quantities[product.id]}
                            >
                                Add to Cart
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
