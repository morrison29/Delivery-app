# Delivery App

Customers describe what they need picked up + a delivery address. The delivery
agent sees incoming orders, updates status, and both sides chat live per-order.

## Local setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # make this the delivery agent account
```

After creating the superuser, go to `/admin/`, open that user, and check
**"Is delivery agent"**. Every other signup via `/accounts/signup/` becomes
a regular customer automatically.

Run locally (uses in-memory channel layer if REDIS_URL isn't set — fine for
one dev process):

```bash
python manage.py runserver
```

## Deploying to Railway or Render

1. Push this repo to GitHub.
2. Create a new project on Railway/Render from the repo.
3. Add a **PostgreSQL** add-on — it sets `DATABASE_URL` automatically on
   Railway; on Render, copy the connection string into an env var named
   `DATABASE_URL`.
4. Add a **Redis** add-on — same deal, sets/needs `REDIS_URL`. This is
   required in production; without it, chat messages won't broadcast
   correctly across multiple server workers.
5. Set environment variables:
   - `SECRET_KEY` — any long random string
   - `DEBUG` — leave unset (defaults to False)
   - `ALLOWED_HOSTS` — your Railway/Render domain, comma-separated if more than one
6. Deploy. The `Procfile`'s `release` line runs migrations automatically on
   each deploy; the `web` line runs the app via `daphne`, which handles both
   normal page loads and the WebSocket chat connections (a plain `gunicorn`
   WSGI server can't do the chat part — that's why we use daphne here).
7. After first deploy, run `python manage.py createsuperuser` via the
   platform's shell/console to create the delivery agent account, then flip
   `is_delivery_agent` to True for that user in `/admin/`.

## App structure

- `accounts/` — custom User model (customer vs delivery agent), signup/login
- `orders/` — Order model, order form, dashboards, status updates
- `chatapp/` — Message model + WebSocket consumer, one chat thread per order
