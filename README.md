# InventoryOS – Reservation Based Inventory Management System

Live App: https://inventory-os-gules.vercel.app

Backend API: https://inventoryos.onrender.com

---

# Overview

InventoryOS is a reservation-based inventory management system built for handling multi-warehouse stock reservations during checkout flows.

The system prevents overselling by temporarily reserving stock before payment confirmation. If the reservation is confirmed, the stock is permanently allocated. If the reservation expires or is cancelled, the stock becomes available again.

This project was built as part of the Allo Engineering Take-Home Exercise.

---

# Problem Statement

During online checkout flows, payment confirmation can take several minutes due to:

* UPI confirmations
* 3DS authentication
* Wallet redirects
* Payment gateway delays

If stock is decremented only after payment succeeds, multiple users may successfully pay for the same inventory unit.

If stock is decremented too early (e.g., at add-to-cart time), abandoned carts artificially reduce inventory visibility and hurt conversions.

To solve this, InventoryOS implements a temporary reservation system.

---

# Features

## Backend Features

* FastAPI backend
* PostgreSQL database hosted on Supabase
* Reservation-based stock locking
* Concurrency-safe reservation logic
* Reservation confirmation endpoint
* Reservation cancellation endpoint
* Automatic expiry support
* REST API architecture
* Hosted publicly on Render

---

## Frontend Features

* Next.js frontend
* Product listing page
* Warehouse-wise stock display
* Reserve stock functionality
* Reservation checkout page
* Live countdown timer
* Confirm purchase flow
* Cancel reservation flow
* Error handling for:

  * 409 Conflict
  * 410 Expired Reservation
* Responsive UI
* Hosted publicly on Vercel

---

# Tech Stack

## Frontend

* Next.js
* React
* TypeScript
* CSS

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* AsyncPG

## Hosting

* Frontend: Vercel
* Backend: Render
* Database: Supabase

---

# Live Deployment

## Frontend

https://inventory-os-gules.vercel.app

## Backend

https://inventoryos.onrender.com

---

# Important Note

The backend is hosted on Render free tier.

Because of Render's free-tier cold starts, the backend may take 1–2 minutes to wake up after inactivity.

If products do not load immediately, please wait briefly and refresh the page.

---

# API Endpoints

## Get Products

GET /api/products

Returns products with warehouse stock information.

---

## Get Warehouses

GET /api/warehouses

Returns warehouse list.

---

## Create Reservation

POST /api/reservations

Creates a temporary reservation for inventory units.

Returns:

* 200 on success
* 409 if stock is unavailable

---

## Confirm Reservation

POST /api/reservations/{id}/confirm

Confirms reservation and permanently allocates stock.

Returns:

* 200 on success
* 410 if reservation expired

---

## Release Reservation

POST /api/reservations/{id}/release

Cancels reservation and releases stock.

---

# Reservation Expiry Strategy

Reservations contain an expiry timestamp.

If the reservation is not confirmed before expiry:

* it becomes invalid
* the stock is released back into inventory

The implementation currently uses expiration validation during reservation confirmation and release operations.

In production, this could be extended using:

* background workers
* cron jobs
* Redis queues
* scheduled cleanup services

---

# Concurrency Handling

The reservation logic is designed to avoid race conditions during simultaneous reservation attempts.

The backend validates available stock before confirming reservations to ensure inventory consistency.

If two users attempt to reserve the final available unit simultaneously:

* one reservation succeeds
* the other receives HTTP 409 Conflict

---

# Running Locally

## Backend

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```txt
http://127.0.0.1:8000
```

---

## Frontend

### Install dependencies

```bash
npm install
```

### Run frontend

```bash
npm run dev
```

Frontend runs on:

```txt
http://localhost:3000
```

---

# Environment Variables

## Frontend

Create `.env.local`

```env
NEXT_PUBLIC_API_URL=https://inventoryos.onrender.com
```

---

# Future Improvements

* Redis-based distributed locking
* Idempotency-Key support
* Authentication
* Admin dashboard
* Real-time stock sync
* Better warehouse selection UX
* Reservation cleanup workers
* Docker deployment
* CI/CD pipeline

---

# Trade-offs

This implementation prioritizes:

* simplicity
* correctness
* deployment speed
* demonstration of reservation flow

Some advanced production optimizations were intentionally simplified to keep the system lightweight and easy to review.

---

# Author

Karan N

---
