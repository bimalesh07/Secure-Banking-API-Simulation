# 🏦 Secure Banking API Simulation
**Core Stack**: Python (Django + DRF), PostgreSQL, Redis, Docker.

## 📌 Project Vision
A simulation-based banking engine focusing on data integrity and enterprise security protocols. This project demonstrates how real-world banks manage complex transactions and human-authorized workflows (Maker-Checker).

## 🛠 Features & Functionalities

### 1. Cloud-Native Infrastructure (Docker)
- **Containerized Services**: 
  - **PostgreSQL**: Primary database with Docker Volumes for persistent financial records.
  - **Redis**: High-speed in-memory store for OTPs and Rate Limiting.
- **Environment Security**: Management of sensitive keys via `.env` files.

### 2. Custom Identity & Role-Based Access (RBAC)
- **Custom User Model**: Built from scratch (using `AbstractBaseUser`) to handle specific identifiers (Email/Phone).
- **The Trinity of Roles**:
  - **User (Customer)**: Can check balance and perform P2P money transfers.
  - **Staff (The Maker)**: Can view accounts and initiate sensitive actions (Deactivate/Delete).
  - **Admin (The Checker)**: Full control. Can create staff and must Approve/Reject all Staff-initiated actions.

### 3. Bulletproof Financial Core
- **Automatic Account Engine**: Generation of unique 12-digit random account numbers.
- **Atomic Transfer Logic**: Using `transaction.atomic` to ensure that if a transfer fails, no money is lost or gained ("All-or-Nothing").
- **Concurrency Handling**: Implementing Pessimistic Locking (`select_for_update`) in PostgreSQL to prevent race conditions during simultaneous transactions.

### 4. Security & Compliance
- **Maker-Checker Workflow**: Sensitive operations (like deleting an account) are not executed directly. They create an `ActionRequest` which requires Admin approval.
- **Redis-Backed OTP**: 6-digit transaction verification OTP with a 5-minute auto-expiry.
- **Idempotency**: Preventing duplicate transactions caused by double-clicks or network retries using unique Request Keys.
- **Account Lookup API**: Real-time name verification of the receiver before confirming a payment (UPI-style).
