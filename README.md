# Django Blog

A full-featured blog application built with Django, following the Corey Schafer tutorial series. Covers the complete Django stack — authentication, media uploads, class-based views, pagination, REST deployment, and more.

**Live:** [arnav-coreyms-django-blog.onrender.com](https://arnav-coreyms-django-blog.onrender.com)

---

## Features

- User registration, login, logout
- Password reset via Gmail SMTP
- User profiles with avatar upload and auto-resize
- Create, update, delete blog posts (author-only)
- Paginated post listing (5 per page)
- Filter posts by author
- Crispy Forms with Bootstrap 4 styling
- Django admin panel
- Deployed on Render with Neon PostgreSQL

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 |
| Database (local) | SQLite |
| Database (production) | PostgreSQL via Neon |
| Auth | Django built-in auth |
| Forms | django-crispy-forms + crispy-bootstrap4 |
| Image handling | Pillow |
| Static files | WhiteNoise |
| Web server | Gunicorn |
| Deployment | Render |
| Secrets | python-dotenv |

---

## Project Structure

```
django_project/
├── blog/                        ← posts app
│   ├── models.py                ← Post model
│   ├── views.py                 ← function + class-based views
│   ├── urls.py                  ← blog URL patterns
│   └── templates/blog/
│       ├── base.html
│       ├── home.html
│       ├── post_detail.html
│       ├── post_form.html       ← shared by create + update
│       ├── post_confirm_delete.html
│       └── user_posts.html
│
├── users/                       ← auth + profile app
│   ├── models.py                ← Profile (OneToOne → User)
│   ├── views.py                 ← register, profile
│   ├── forms.py                 ← UserRegisterForm, UserUpdateForm, ProfileUpdateForm
│   ├── signals.py               ← auto-create Profile on user save
│   └── templates/users/
│       ├── register.html
│       ├── login.html
│       ├── logout.html
│       ├── profile.html
│       └── password_reset*.html (4 templates)
│
├── django_project/              ← project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── .env                         ← secrets (not in git)
├── .gitignore
├── manage.py
├── requirements.txt
└── posts.json                   ← sample post data
```

---

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/Arnav-Naive/CoreySchafer_django_project.git
cd CoreyShafer_django_project/django_project

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 2. Create `.env` (next to `manage.py`)

```env
SECRET_KEY=your-django-secret-key
EMAIL_USER=your@gmail.com
EMAIL_PASS=your-gmail-app-password
# DATABASE_URL=your-neon-connection-string  ← comment out for local SQLite
```

### 3. Run migrations and start

```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open `http://127.0.0.1:8000`

### 4. Load sample posts (optional)

```bash
python manage.py shell
```
```python
import json
from blog.models import Post
from django.contrib.auth.models import User

with open('posts.json') as f:
    posts = json.load(f)

for p in posts:
    Post.objects.create(title=p['title'], content=p['content'], author_id=p['user_id'])
```

---

## Deployment (Render + Neon)

### Architecture

```
Local → git push → GitHub (public repo)
                       ↓ auto-deploy
                    Render (gunicorn)
                       ↓
                    Neon (PostgreSQL)
```

### Steps

1. **Neon** — create a project at [neon.tech](https://neon.tech), copy the connection string
2. Uncomment `DATABASE_URL` in `.env`, run `python manage.py migrate`, re-comment it
3. Run `python manage.py createsuperuser` while `DATABASE_URL` is active
4. **Render** — new Web Service, connect the GitHub repo:
   - Root Directory: `django_project`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn django_project.wsgi`
   - Instance Type: Free
5. Add environment variables on Render dashboard: `SECRET_KEY`, `EMAIL_USER`, `EMAIL_PASS`, `DATABASE_URL`

Every `git push` auto-deploys. No manual steps.

---

## Gmail App Password Setup

Required for password reset emails.

1. Go to [myaccount.google.com](https://myaccount.google.com) → Security
2. Enable 2-Step Verification
3. App Passwords → create one named "Django" → copy the 16-character password
4. Set `EMAIL_PASS` in `.env` and in Render environment variables

> For local testing without sending real emails, swap `EMAIL_BACKEND` in `settings.py` to `django.core.mail.backends.console.EmailBackend` — emails will print in the terminal instead.

---

## Key Concepts Covered

**Signals** — `post_save` on User auto-creates a Profile. Wired in `apps.py` via `ready()`.

**OneToOneField** — Profile extends User without modifying the built-in model.

**CBVs with Mixins** — `LoginRequiredMixin` for auth gates, `UserPassesTestMixin` for author-only edit/delete.

**`instance=` on forms** — passes existing object to update instead of create. Without this, form saves create duplicate records.

**`request.FILES` + `enctype`** — both required for image uploads. Missing either silently breaks the upload.

**Image resize** — handled in `Profile.save()` using Pillow. Keeps uploaded images at max 300×300 to avoid storage bloat.

**Pagination** — `paginate_by = 5` on `ListView`. Template uses `page_obj` (not `page.obj` — a typo that breaks highlighting).

**Media vs Static** — static files (CSS/JS) are handled by WhiteNoise; media files (uploads) need `MEDIA_ROOT`/`MEDIA_URL` and a dev-only URL rule in `urls.py`.

**Database switching** — `dj_database_url.config()` reads `DATABASE_URL` if set (Neon), falls back to SQLite if not. Same codebase works locally and in production.

---

## .gitignore

```
.env
*.pyc
__pycache__/
db.sqlite3
media/
.venv/
staticfiles/
```

Never commit `.env`. If you accidentally do on a public repo — immediately invalidate the leaked credential (delete the Gmail App Password), generate a new one, and purge the file from git history with `git filter-branch`.

---

## Requirements

```
Django>=6.0
Pillow>=10.0
gunicorn
whitenoise
dj-database-url
psycopg2-binary
django-crispy-forms
crispy-bootstrap4
python-dotenv
```