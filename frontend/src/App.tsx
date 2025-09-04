import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { CreateOrderPage } from './pages/CreateOrderPage';
import { OrdersPage } from './pages/OrdersPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="nav-bar">
          <Link to="/" className="nav-link">Create Order</Link>
          <Link to="/orders" className="nav-link">Orders</Link>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<CreateOrderPage />} />
            <Route path="/orders" element={<OrdersPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
