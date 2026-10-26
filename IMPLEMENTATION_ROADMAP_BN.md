# NOVAMART — সম্পূর্ণ মার্কেটপ্লেসে যাওয়ার ধাপ

## ধাপ ১ — ভিত্তি ও অ্যাকাউন্ট
- [x] Responsive storefront starter
- [x] Django + PostgreSQL modular foundation
- [x] Register/login API, password hashing and password validation
- [x] Login/register/password-reset throttling
- [x] Token-based password reset flow (development email prints to backend terminal)
- [x] Basic customer/seller role field
- [ ] Email/phone verification with expiry, one-time use and resend throttles
- [ ] Password reset and session flow end-to-end test on real HTTPS domains
- [ ] Admin MFA and recovery procedure

## ধাপ ২ — গ্রাহক
- Customer profile, saved addresses, phone verification
- Search, category filters, sort, pagination, product detail, image gallery
- Persistent cart, wishlist, reviews with moderation
- Checkout validation, COD eligibility, order history/tracking
- Order confirmation email/SMS

## ধাপ ৩ — সেলার
- Seller application/KYC review and approval by admin
- Seller-only product CRUD and image uploads
- Inventory adjustments and low-stock alerts
- Seller order fulfilment view, shipping label, returns handling
- Commission rules, seller balance ledger, payout requests and reconciliation
- Object-level permissions on every seller endpoint (never trust client-sent seller/user IDs)

## ধাপ ৪ — অর্ডার, টাকা ও ডেলিভারি
- Transaction-safe checkout, stock locking/reservation and idempotency
- Order status state machine and audit history
- Payment gateway integration via official merchant account
- Verify webhook signatures, prevent duplicate events, reconcile settlements/refunds
- Courier API integration, tracking updates, shipping fees by zone/weight
- COD reconciliation and fraud/risk review

## ধাপ ৫ — অ্যাডমিন ও অপারেশন
- Dashboard metrics, roles and least-privilege permissions
- Manage users/sellers/products/categories/orders/refunds/coupons/banners
- Commission/tax/shipping rules, support tickets, moderation and audit logs
- Admin action confirmation and immutable audit trail for sensitive changes

## ধাপ ৬ — নিরাপত্তা ও স্কেল
- HTTPS-only, secure cookies, CSRF, strict allowed hosts and CORS
- Redis-backed throttling/cache and background jobs (email/SMS, thumbnails, notifications)
- WAF/bot mitigation, CAPTCHA only when risk warrants, anomaly alerts
- DB indexes, query profiling, connection pooling, backups and restore drills
- Object storage/CDN for media, logs/metrics/traces, uptime alerts
- Automated unit/API/integration tests, load tests, dependency scans and independent security review
- Staging environment, migration rollback plan and documented incident response

## ডেটাবেজ পরিকল্পনা
প্রথমে PostgreSQL-এ domain-separated apps এবং সঠিক indexes/constraints ব্যবহার করা হবে। Users, products, orders, order items, payments, inventory ledger, commissions/payouts, shipping, reviews ও audit events আলাদা টেবিল/মডিউলে থাকবে। প্রথম দিন থেকেই আলাদা আলাদা database না করে প্রয়োজনমতো cache, read replicas, background workers এবং পরে traffic/ownership-এর ভিত্তিতে service/database separation করা বেশি বাস্তবসম্মত।

## বাস্তব অবস্থা
এই ZIP-এ register/login/reset-এর ভিত্তি ও data models আছে, কিন্তু সম্পূর্ণ marketplace checkout, seller permissions, payment/shipping integrations, test suite এবং production security review এখনো নেই। তাই একে production-ready বলে চালু করবেন না। Live email, payment gateway বা SMS-এর credentials ZIP-এ রাখা হয়নি।
