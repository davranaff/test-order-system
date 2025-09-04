db = db.getSiblingDB('restaurant_db');

db.dropDatabase();
db.createCollection('products');
db.createCollection('orders');

db.products.createIndex({ "name": 1 });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "is_available": 1 });

db.orders.createIndex({ "status": 1 });
db.orders.createIndex({ "customer.name": 1 });
db.orders.createIndex({ "created_at": -1 });
db.orders.createIndex({ "customer.phone": 1 });

db.products.insertMany([
    {
        _id: UUID("b7b14f78-07f6-4958-b042-f4dfda5544c2"),
        name: "Пицца Маргарита",
        price: 450.0,
        category: "Пицца",
        is_available: true,
        description: "Классическая пицца с томатным соусом, моцареллой и базиликом",
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: UUID("b7b14f78-07f6-4958-b042-f4dfda5544ca"),
        name: "Паста Карбонара",
        price: 380.0,
        category: "Паста",
        is_available: true,
        description: "Традиционная итальянская паста с беконом и сыром",
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: UUID("b7b14f78-07f6-4958-b042-f4dfda5544cc"),
        name: "Цезарь с курицей",
        price: 320.0,
        category: "Салаты",
        is_available: true,
        description: "Салат с куриной грудкой, сыром пармезан и соусом цезарь",
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        _id: UUID("b7b14f78-07f6-4958-b042-f4dfda5544cf"),
        name: "Тирамису",
        price: 180.0,
        category: "Десерты",
        is_available: false,
        description: "Классический итальянский десерт",
        created_at: new Date(),
        updated_at: new Date()
    }
]);
