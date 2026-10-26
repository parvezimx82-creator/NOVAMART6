# NOVAMART — Marketplace MVP Foundation

বাংলাদেশ-কেন্দ্রিক multi-vendor marketplace-এর উন্নত ডেভেলপমেন্ট ভিত্তি। এটি এখনও সম্পূর্ণ production-ready marketplace নয়।

## চালাতে
1. Docker Desktop/Engine ইনস্টল করুন।
2. `.env.example` কপি করে `.env` বানান।
3. `.env`-এ `DJANGO_SECRET_KEY` ও database password বদলান।
4. `docker compose up --build` চালান।
5. Frontend: http://localhost:3000
6. Django admin তৈরি করতে অন্য terminal-এ:
   `docker compose exec backend python manage.py createsuperuser`
7. Admin: http://localhost:8000/admin/
8. API health: http://localhost:8000/api/health/

Compose backend startup-এ development migration তৈরি করে migrate করার চেষ্টা করে। Production-এ migration files version control-এ রেখে review করা উচিত; production container startup-এ স্বয়ংক্রিয় `makemigrations` চালাবেন না।

## Included
- Premium-style responsive storefront UI (demo products)
- Register, login, forgot-password and reset-password screens
- Django password hashing and minimum password validation
- Login/register/password-reset throttling, Axes lockout configuration
- PostgreSQL, modular Django apps for accounts/catalog/orders
- Customer/seller role field and initial product/order/category models
- Django Admin management foundation

## Known gaps
- Demo storefront products are not yet loaded from the catalog API.
- Basic localStorage cart, checkout and transactional order creation are included; they still require end-to-end verification.
- Seller-only API permissions and seller onboarding approval are not complete.
- Password reset email is printed by development console backend; configure and verify a real transactional email provider before launch.
- CSRF/session behavior must be tested end-to-end on intended HTTPS domains.
- Email/SMS OTP, MFA, payment gateway, shipping provider, refund/payout flows, automated tests, monitoring and production hardening remain to be completed.

## Security
Never deploy with `DEBUG=True`, sample secrets, default passwords or HTTP-only production. Configure HTTPS, secure cookies, allowed hosts, CORS/CSRF, rate limits, MFA for privileged accounts, logs, backups, dependency updates and security review. Rate limiting can be weakened by incorrectly configured reverse-proxy client IP forwarding; configure proxy trust carefully.


## New in the updated package
- Floating customer-support chat widget with stored conversations and Django Admin replies (polling MVP).
- Configurable payment-method catalog for COD, bKash, Nagad, Rocket, upay, Visa Card, and USDT on BSC (BEP20).
- Payment submission/reference records for manual review; real provider checkout/webhooks still require merchant credentials and integration.
- See `PAYMENTS_AND_LIVE_CHAT_BN.md` for Bengali setup instructions and limitations.

- Added API-backed product listing/search, browser-persistent cart, checkout form, transactional order creation and stock decrement.
- Added basic order tests in `backend/orders/tests.py`; run them in a configured Django/PostgreSQL environment.


## Render deployment
See `RENDER_DEPLOY_BN.md` for the current Render settings and required environment variables.
## Responsive design & required services
See `RESPONSIVE_AND_SERVICES_BN.md` for the phone/tablet/desktop layout updates and the hosting, database, payment, email/SMS, courier and security services needed before launch.
