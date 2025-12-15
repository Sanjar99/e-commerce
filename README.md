# e-commerce


Marketplace backend modeliga asoslangan to‘liq API dokumentatsiya va JSON response misollari. Shu orqali frontendchi har bir endpoint va ma’lumot strukturasini aniq tushunadi.

1️⃣ User / Authentication
Endpoint: /api/users/

Method: GET
Description: Foydalanuvchi ro‘yxati
Response Example:

[
  {
    "id": 1,
    "username": "sanjar",
    "email": "sanjar@example.com",
    "phone": "+998901234567",
    "first_name": "Sanjar",
    "last_name": "Ruzmanov"
  }
]

Endpoint: /api/users/{id}/

Method: GET
Description: Bitta foydalanuvchi ma’lumotlari
Response Example:

{
  "id": 1,
  "username": "sanjar",
  "email": "sanjar@example.com",
  "phone": "+998901234567",
  "first_name": "Sanjar",
  "last_name": "Ruzmanov"
}

2️⃣ Seller
Endpoint: /api/sellers/

Method: GET
Description: Seller ro‘yxati
Response Example:

[
  {
    "id": 1,
    "shop_name": "Super Electronics",
    "shop_slug": "super-electronics",
    "description": "Elektronika do‘koni",
    "is_verified": true,
    "rating": 4.5
  }
]

Endpoint: /api/sellers/{id}/

Method: GET
Description: Bitta seller tafsilotlari
Response Example:

{
  "id": 1,
  "shop_name": "Super Electronics",
  "shop_slug": "super-electronics",
  "description": "Elektronika do‘koni",
  "is_verified": true,
  "rating": 4.5,
  "balance": 1200.50,
  "pending_amount": 300.00
}

3️⃣ Product
Endpoint: /api/products/

Method: GET
Description: Barcha productlar
Response Example:

[
  {
    "id": 1,
    "name": "iPhone 15",
    "slug": "iphone-15",
    "description": "Apple iPhone 15, 256GB",
    "price": "1200.00",
    "brand": "Apple",
    "stock": 10,
    "rating": 4.8,
    "category": "Smartphones",
    "main_image": "http://example.com/media/product_main_images/iphone15.jpg",
    "variants": [
      {"type": "Color", "value": "Red"},
      {"type": "Storage", "value": "256GB"}
    ],
    "seller_products": [
      {
        "seller": "Super Electronics",
        "price": "1200.00",
        "old_price": "1300.00",
        "stock": 5
      }
    ]
  }
]

Endpoint: /api/products/{id}/

Method: GET
Description: Bitta product tafsilotlari
Response Example:

{
  "id": 1,
  "name": "iPhone 15",
  "slug": "iphone-15",
  "description": "Apple iPhone 15, 256GB",
  "price": "1200.00",
  "brand": "Apple",
  "stock": 10,
  "rating": 4.8,
  "category": "Smartphones",
  "main_image": "http://example.com/media/product_main_images/iphone15.jpg",
  "variants": [
    {"type": "Color", "value": "Red"},
    {"type": "Storage", "value": "256GB"}
  ],
  "seller_products": [
    {
      "seller": "Super Electronics",
      "price": "1200.00",
      "old_price": "1300.00",
      "stock": 5
    }
  ],
  "images": [
    "http://example.com/media/product_images/iphone15_1.jpg",
    "http://example.com/media/product_images/iphone15_2.jpg"
  ]
}

4️⃣ Cart
Endpoint: /api/cart/

Method: GET
Description: Foydalanuvchi cartini olish
Response Example:

{
  "id": 1,
  "user": "sanjar",
  "items": [
    {
      "product": "iPhone 15",
      "seller": "Super Electronics",
      "quantity": 2,
      "price_at_that_moment": "1200.00"
    }
  ]
}

5️⃣ Order
Endpoint: /api/orders/

Method: GET
Description: Foydalanuvchi orderlari
Response Example:

[
  {
    "id": 1,
    "order_number": "ORD-20251215-001",
    "total_price": "2400.00",
    "total_items": 2,
    "status": "Pending",
    "is_paid": false,
    "shipping_address": "Tashkent, Shayxontohur",
    "seller_groups": [
      {
        "seller": "Super Electronics",
        "seller_total_price": "2400.00",
        "status": "Awaiting",
        "items": [
          {
            "product": "iPhone 15",
            "quantity": 2,
            "price": "1200.00"
          }
        ]
      }
    ]
  }
]

6️⃣ Payment
Endpoint: /api/payments/{order_id}/

Method: GET
Description: Order uchun to‘lov ma’lumotlari
Response Example:

{
  "order": "ORD-20251215-001",
  "payment_id": "PAY-123456",
  "amount": "2400.00",
  "status": "pending",
  "paid_at": null
}

7️⃣ Review
Endpoint: /api/reviews/{product_id}/

Method: GET
Description: Bitta productga yozilgan reviewlar
Response Example:

[
  {
    "user": "sanjar",
    "rating": 5,
    "comment": "Great phone!",
    "created_at": "2025-12-15T18:00:00Z"
  }
]

8️⃣ Wishlist
Endpoint: /api/wishlist/

Method: GET
Response Example:

[
  {
    "user": "sanjar",
    "items": [
      {"product": "iPhone 15"},
      {"product": "MacBook Pro"}
    ]
  }
]

9️⃣ Notification
Endpoint: /api/notifications/

Method: GET
Response Example:

[
  {
    "title": "Order Shipped",
    "message": "Your order ORD-20251215-001 has been shipped",
    "type": "Order",
    "is_read": false,
    "created_at": "2025-12-15T18:05:00Z"
  }
]