# Project No - 11: Household Service Providing Platform

A Django + DRF implementation for a household services marketplace (e.g., House Shifting, Home Cleaning) with two roles: **Admin** and **Client**.

## Features (Mapped to Marking Scheme)

1. **User Authentication (15 Marks)**
   - Registration & Login (JWT)
   - User profile management (bio, profile image URL, socials)
   - Roles: Admin and Client

2. **Admin Creation (15 Marks)**
   - Admins can promote/demote users to **Admin**
   - Only Admins can create other Admins (role change endpoint)

3. **Client Profile (15 Marks)**
   - View client info & service (order) history
   - Update profile fields: bio, avatar URL, social links

4. **Add to Cart (15 Marks)**
   - Add services to a cart (before order)
   - Remove services from the cart
   - Checkout converts cart to Order

5. **Reviews & Ratings (10 Marks)**
   - Leave rating (out of 5) and review after receiving a service
   - Average rating per service
   - Sort services by rating

6. **Future Payment Gateway (Placeholder)**
   - Order has `payment_status` and `payment_ref` fields for future integration

7. **Deployment & Submission (10 Marks)**
   - Ready for deployment (Render/Railway)
   - Documentation included in this README

---

## Quick Start (Local)

1. **Create virtualenv & install deps**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment**
   ```bash
   cp .env.example .env
   # edit SECRET_KEY, DEBUG, etc. as needed
   ```

3. **Init DB**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # create initial admin
   ```

4. **Run dev server**
   ```bash
   python manage.py runserver
   ```

5. **Browse**
   - API root: `http://127.0.0.1:8000/api/`
   - Admin: `http://127.0.0.1:8000/admin/`

## Core API Endpoints

### Auth & Profile
- `POST /api/auth/register/` (email, password, first_name?, last_name?)
- `POST /api/auth/login/` (JWT obtain)
- `GET  /api/auth/me/` (current user)
- `GET  /api/profile/me/` (my profile)
- `PUT  /api/profile/me/` (update bio, avatar_url, socials)
- `GET  /api/profile/me/history/` (my orders history)

### Admin-only
- `GET  /api/admin/users/`
- `PATCH /api/admin/users/{id}/role/` → `{ "role": "ADMIN" | "CLIENT" }`
- `GET  /api/admin/orders/`
- `PATCH /api/admin/orders/{id}/status/` → `{ "status": "CONFIRMED" | "FULFILLED" | "CANCELLED" }`

### Services
- `GET  /api/services/` (supports `?ordering=-avg_rating` and `?search=clean`)
- `GET  /api/services/{slug}/`

### Cart & Orders
- `GET  /api/cart/` (current open cart)
- `POST /api/cart/add/` → `{ "service_slug": "...", "quantity": 1 }`
- `POST /api/cart/remove/` → `{ "item_id": <id> }`
- `POST /api/orders/checkout/` → creates order from cart

### Reviews
- `GET  /api/services/{slug}/reviews/`
- `POST /api/services/{slug}/reviews/` → `{ "rating": 5, "comment": "Great!" }`
- `PUT/PATCH/DELETE /api/reviews/{id}/` (author-only)

## Deployment Notes (Render/Railway)

- Use **Gunicorn** and set `DJANGO_SETTINGS_MODULE=household.settings`
- Set environment variables from `.env`
- Use PostgreSQL add-on (set `DATABASE_URL`)
- `python manage.py migrate` on deploy
- Optionally `python manage.py collectstatic` for static assets

## Payment Gateway Placeholder

- Order fields `payment_status`, `payment_ref` are ready
- In future: add "Create Payment Intent" and webhook handler, then mark `payment_status`

---

**Made for academic submission.**
