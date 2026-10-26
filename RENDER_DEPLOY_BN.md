# NOVAMART — Render Deployment Guide (Django backend)

> The archive contains separate `frontend/` and `backend/` folders. Deploy them as separate services. The backend service must use the `backend` folder as its Root Directory when the repository preserves this project folder structure.

## 1. Web Service settings
- Runtime: **Python 3**
- Branch: the branch that contains the uploaded source (usually `main`)
- Root Directory: `NOVAMART_Complete_MVP/backend` if the outer folder name is present in GitHub; otherwise `backend` if `backend/` is directly at repository root; leave blank only if `manage.py` is at repository root.
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Start Command: `python manage.py migrate --noinput && python manage.py seed_payment_methods && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

Migrations are run at start because the production database may not be available during the build phase. This project currently does not include committed migration files for every custom app; before a production launch, create and commit migrations (`python manage.py makemigrations accounts catalog orders payments livechat`) and then deploy again. Do not rely on `--run-syncdb` as a permanent production migration strategy.

## 2. Create PostgreSQL first
Create a PostgreSQL database in Render and copy its connection values into backend Environment Variables. Use the internal hostname for services in the same region:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT` (normally `5432`)

Do not paste credentials into GitHub or chat.

## 3. Environment Variables for backend
- `DJANGO_SECRET_KEY`: unique, long random secret
- `DJANGO_DEBUG`: `False`
- `DJANGO_ALLOWED_HOSTS`: backend hostname only, no scheme, e.g. `novamart-api.onrender.com`
- `CORS_ALLOWED_ORIGINS`: exact frontend origin, e.g. `https://novamart-web.onrender.com`
- `CSRF_TRUSTED_ORIGINS`: exact frontend origin including `https://`
- `FRONTEND_BASE_URL`: exact frontend origin including `https://`
- Database variables listed above

Do not use `ALLOWED_HOSTS=['*']` in production. This settings file intentionally requires a non-empty host allowlist, secret key, and database configuration on Render.

## 4. Admin account
After the backend deploys, open Render's Shell for the backend service (if available) and run:
`python manage.py createsuperuser`

If Shell is not available on your plan, create the superuser using a one-off job or a temporary protected management workflow, then remove that workflow. Never put a permanent admin password in source code or public environment files. Admin URL: `https://YOUR-BACKEND-HOST/admin/`.

## 5. Verify after deploy
- `https://YOUR-BACKEND-HOST/api/health/` should return JSON with `status: ok`.
- Open `/admin/` and verify CSS loads (WhiteNoise handles collected static files).
- Check Render logs for migration/database errors.
- Test login, catalog, checkout, order status, payment review, and permissions before public launch.

## Important limits
The UI's payment options do not enable live payment processing. Live bKash/Nagad/Rocket/upay/card payments require approved provider merchant/API integration and verified callbacks. USDT support here is limited to BNB Smart Chain (BSC/BEP20) with manual verification until a secure verifier is implemented. A successful deployment does not by itself prove the marketplace is production-ready; security review, migrations, backups, email, authorization tests and end-to-end tests are still required.
