### 📦 Telegram Ecommerce Bot – Optimal Structure
### https://excalidraw.com/#json=ubHKlQNV2_uBFENtNAlaQ,gjaDg0l9qnTnhBBAj2h2ow
```
ecommerce_bot/
│
├── bot/                      # Telegram bot logic
│   ├── handlers/             # User interaction handlerlar
│   │   ├── start.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── support.py
│   │
│   ├── keyboards/            # Tugmalar
│   │   ├── reply.py
│   │   └── inline.py
│   │
│   ├── states/               # FSM state lar
│   │   └── checkout_state.py
│   │
│   └── bot.py                # Dispatcher va handler register
│
├── services/                 # Business logic
│   ├── product_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   └── user_service.py
│
├── repositories/             # Database bilan ishlash
│   ├── product_repo.py
│   ├── cart_repo.py
│   ├── order_repo.py
│   └── user_repo.py
│
├── models/                   # ORM modellar
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
│
├── database/
│   ├── connection.py
│   └── session.py
│
├── config.py                 # Token va sozlamalar
├── main.py                   # Bot entry point
├── requirements.txt
└── README.md
```
