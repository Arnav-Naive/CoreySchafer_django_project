## Part 6 — User Registration

-> It’s better to make a separate **users app** for handling registration and user-related features instead of mixing everything inside blog.

---

### 1. Create Users App

```bash
python manage.py startapp users
```

---

### 2. Do some settings (`settings.py`)

We need to tell Django that our new app exists.

```python
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',   # from users/apps.py
]
```

---

### 3. Let’s start with the views (logic part)

-> This will handle the logic for the register route
-> We won’t create URL patterns yet, just focus on logic first

```python
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
```

---

### 4. Create template for register page

We need a UI to show the form.

Structure:

```
users/
 └── templates/
      └── users/
           └── register.html
```

-> Make sure folder naming is exact, otherwise Django won’t find it.

Inside `register.html`:

```html
<!-- extend base template -->
```

---

### 5. Now we need a URL pattern

-> So we can actually visit this page in browser

Earlier in blog app we created separate `urls.py`
We *could* do same here, but for now keep it simple

👉 Import view directly into project’s main `urls.py`

File: `django_project/urls.py`

```python
from users import views as user_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
]
```

---

### 6. Add POST request handling (form submission)

Right now form only displays, doesn’t save anything.

Update `views.py`:

```python
from django.contrib import messages
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()   # saves user to database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
```

-> `form.save()` → creates user in database (visible in admin)

---

### 7. Add email field (custom form)

Default form doesn’t include email → we extend it.

Create `users/forms.py`:

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

---

### 8. Update views to use custom form

```python
from .forms import UserRegisterForm
```

Replace:

```python
UserCreationForm
```

with:

```python
UserRegisterForm
```

---

### 9. Styling using crispy forms

-> Default Django forms look ugly
-> Use crispy forms for better UI

Install:

```bash
pip install django-crispy-forms
pip install crispy-bootstrap4
```

---

Update `settings.py`:

```python
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'crispy_bootstrap4',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

---

### 10. Update template (`register.html`)

```html
{% load crispy_forms_tags %}

<form method="POST">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Sign Up</button>
</form>
```

---

### Final Result

* Registration page works
* User gets saved in database
* Email field included
* Form looks clean (bootstrap styling)

---

### Mistakes I made (important)

* Used wrong import (`form` instead of `forms`)
* Wrong template path
* Forgot `crispy-bootstrap4`

→ These caused most of the errors





## Part 7 — Login and Logout System

### Timeline (what happens in this part)

* Built-in login/logout views
* URL setup
* Templates
* Redirect handling
* Navbar logic
* Protected routes
* Profile page
* `login_required` + `?next=`

---

### 1. Using Django’s built-in login/logout views

-> Instead of writing login logic manually, Django already provides it

In `django_project/urls.py`:

```python id="p9v4xk"
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
```

👉 `as_view()` → converts class-based view to callable

---

### 2. Create templates

Create:

```id="9c2xlt"
users/templates/users/login.html
users/templates/users/logout.html
```

---

### 3. Why `/accounts/profile/` appears

When login succeeds, Django redirects to:

```id="s5px6n"
/accounts/profile/
```

👉 This is Django’s **default redirect URL**

---

### Fix it (important)

In `settings.py`:

```python id="1qz8xg"
LOGIN_REDIRECT_URL = 'blog-home'
```

Now after login → user goes to homepage

---

### 4. Redirect to login after register

In `users/views.py`:

```python id="1kwgqf"
messages.success(request, 'Your account has been created! You can now log in.')
return redirect('login')
```

👉 Makes logical flow:
Register → Login → Home

---

### 5. Logout template

Simple page shown after logout:

```html id="dpb2ij"
{% extends "blog/base.html" %}

{% block content %}
    <h2>You have been logged out</h2>
    <a href="{% url 'login' %}">Log in again</a>
{% endblock %}
```

---

### 6. Change navbar based on login state

Use built-in variable:

```python id="9vxr6t"
user.is_authenticated
```

Example:

```html id="m3j0nl"
{% if user.is_authenticated %}
    <a href="{% url 'profile' %}">Profile</a>

    <form method="POST" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">Logout</button>
    </form>
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
{% endif %}
```

---

### 7. Built-in user object

Django automatically gives:

```python id="8s7vpf"
user
```

Contains:

* username
* email
* authentication status

---

### 8. Restrict access to certain routes

Problem:
👉 Anyone can open `/profile/` directly

Solution:

```python id="r4djqj"
from django.contrib.auth.decorators import login_required
```

---

### 9. Create profile view

`users/views.py`:

```python id="tuyg8z"
@login_required
def profile(request):
    return render(request, 'users/profile.html')
```

---

### 10. Create profile template + URL

Template:

```id="7b6h3r"
users/templates/users/profile.html
```

URL:

```python id="yzp7nr"
path('profile/', user_views.profile, name='profile')
```

---

### 11. Set login URL (important)

If user is not logged in → where to redirect?

In `settings.py`:

```python id="kq0c8f"
LOGIN_URL = 'login'
```

---

### 12. What is `?next=...`

Example:

```id="7k1y1r"
/login/?next=/profile/
```

👉 Meaning:

* User tried to access `/profile/`
* Not logged in → redirected to login
* After login → automatically sent back to `/profile/`

---

### Why this matters

Without `?next=`:

* user logs in → always goes to home
  With `?next=`:
* user returns to original page

---

### Final flow (full picture)

1. User clicks profile
2. Not logged in → redirected:

   ```
   /login/?next=/profile/
   ```
3. User logs in
4. Django redirects back → `/profile/`

---

### Common mistakes I made

* typo: `templates_names` ❌ → `template_name` ✅
* forgot `LOGIN_REDIRECT_URL`
* didn’t understand `/accounts/profile/`
* forgot `login_required`

---

### Part 8  User Profile and Picture
![alt text](image.png)
OR
## Part 8 — User Profile and Picture

### 0. Goal

-> Each user should have:

* profile page
* profile picture
* extra data (not inside default User model)

---

### 1. Profile Model (One-to-One relation)

`users/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
```

---

### Why `__str__` is used

```python
def __str__(self):
```

👉 Controls how object is displayed in:

* Django admin
* shell

Without it:

```
Profile object (1) ❌
```

With it:

```
ArnavF Profile ✅
```

---

### Why OneToOneField

```python
user = models.OneToOneField(User)
```

👉 Each user → exactly ONE profile
👉 Extends default Django User model cleanly

---

### 2. Migrations

You must apply changes to database:

```bash
pip install pillow   # required for ImageField

python manage.py makemigrations
python manage.py migrate
```

---

### Why Pillow?

👉 Django cannot handle images without it
👉 `ImageField` depends on Pillow internally

---

### 3. Test in Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.filter(username='ArnavF').first()
user.profile
user.profile.image
user.profile.image.url
```

👉 This proves:

* Profile is linked automatically
* Image works

---

### 4. Media Settings (`settings.py`)

```python
import os

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

---

### Why this is needed

* Uploaded images are NOT static files
* Django needs:

  * where to store → `MEDIA_ROOT`
  * how to access → `MEDIA_URL`

---

### 5. Profile Template

`users/templates/users/profile.html`

```html
{% extends "blog/base.html" %}

{% block content %}
<div class="content-section">
    <div class="media">
        <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
        <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
        </div>
    </div>
</div>
{% endblock %}
```

---

### 6. Add Media URL Handling

`django_project/urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### Why this is needed

👉 During development:

* Django does NOT serve media files automatically
* This line tells Django:
  “Serve images from /media/ folder”

👉 Without this:

* images won’t load in browser ❌

---

### 7. Signals (important concept)

Create `users/signals.py`

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

---

### Why signals are needed

Problem:
👉 When a new User is created → Profile is NOT automatically created

Solution:
👉 Signals listen to events

* `post_save` → runs after user is saved
* `create_profile` → creates Profile automatically
* `save_profile` → keeps it updated

---

### Without signals

```python
user.profile ❌ (error)
```

### With signals

```python
user.profile ✅ works automatically
```

---

### 8. Connect signals (`apps.py`)

`users/apps.py`

```python
class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        import users.signals
```

---

### Why this is required

👉 Django won’t run signals unless they are imported

`ready()` ensures:

* signals are loaded when app starts

---

### 9. Default Image

Place:

```id="e4q7tr"
media/default.jpg
```

👉 Used when user has no uploaded image

---

### Final Flow

1. User registers
2. Signal creates Profile automatically
3. Default image assigned
4. User visits profile page
5. Image + data displayed

---

### Common mistakes I made

* forgot Pillow → ImageField crashes
* forgot signals → `user.profile` error
* forgot media URL → image not loading
* wrong path for default image

---

### Core Understanding (important)

* User model = authentication
* Profile model = extra data
* OneToOne = extension
* Signals = automation
* Media = user-uploaded content

---


```That covers everything in Part 8 cleanly. A few things worth locking in mentally before moving on:
Signals are the trickiest part here. The pattern — "run my code when Django's built-in code does something" — comes up a lot. The apps.py import is easy to forget and it'll silently break things (no error, profiles just won't get created).
The if settings.DEBUG media URL line is dev-only scaffolding. Don't carry it into production thinking it's how media files work. It isn't.
OneToOneField vs ForeignKey — a common confusion point. ForeignKey allows one user → many profiles. OneToOneField enforces exactly one. You always want OneToOneField for user profiles.
```

## Part 9 — Update User Profile

### 0. Goal

-> Allow user to:

* update username/email
* update profile image

---

### 1. Forms (`users/forms.py`)

We split forms because:

* User data → `User` model
* Profile data → `Profile` model

```python id="9v8p0c"
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
```

---

### Why two forms?

👉 One model cannot handle both:

* User fields
* Profile image

So we use:

```id="q4k1gh"
UserUpdateForm + ProfileUpdateForm
```

---

### 2. View Logic (`views.py`)

```python id="r7m3zs"
if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)

    p_form = ProfileUpdateForm(
        request.POST,
        request.FILES,
        instance=request.user.profile
    )

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, 'Your account has been updated!')
        return redirect('profile')

else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

context = {
    'u_form': u_form,
    'p_form': p_form
}

return render(request, 'users/profile.html', context)
```

---

### Critical concept (you skipped this)

```python id="m2ph1y"
instance=request.user
```

👉 This means:

* UPDATE existing user
* NOT create new user

Without this:
👉 duplicate users will be created ❌

---

### Why `request.FILES`?

```python id="fjh3l7"
request.FILES
```

👉 Required for file uploads (image)

Without it:

* image won’t upload
* form silently fails

---

### 3. Template (`profile.html`)

```html id="1gh4kq"
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}

    <fieldset class="form-group">
        <legend>Profile Info</legend>
        {{ u_form|crispy }}
        {{ p_form|crispy }}
    </fieldset>

    <button type="submit">Update</button>
</form>
```

---

### Why `enctype` is critical

```html id="2c92yo"
enctype="multipart/form-data"
```

👉 Without this:

* file upload = broken ❌

---

### 4. Image Resize (Model level)

`models.py`

```python id="b6zv0m"
from PIL import Image

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        img.thumbnail((300, 300))
        img.save(self.image.path)
```

---

### Why resize?

Without this:

* users upload 5MB+ images
* slows site
* wastes storage

---

### 5. Display profile image in posts

`home.html`

```html id="5o0z8j"
<img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}">
```

---

### Why this works

```python id="9b3k4x"
post → author → profile → image
```

Chain:

* Post → User
* User → Profile
* Profile → Image

---

### Final flow

1. User opens profile page
2. Form pre-filled using `instance=`
3. User updates info + uploads image
4. Form submits → POST
5. Data saved
6. Image resized
7. UI updates everywhere

---

### Core understanding (real takeaway)

* Forms = bridge between HTML and models
* `instance=` = update vs create
* `FILES` + `enctype` = required for uploads
* Image resize = performance control

---

##  Part 10 - Class based views,View,Update,Delete using this views(Create,Update,Delete Posts)
## Part 10 — Class-Based Views (CRUD for Posts)

### 0. Why Class-Based Views (CBV)?

-> Instead of writing repetitive functions
-> Django gives ready-made classes for common patterns

Examples:

* ListView → show list
* DetailView → show single object
* CreateView → create object
* UpdateView → update
* DeleteView → delete

---

### 1. List View (Home Page)

```python id="1qv7xk"
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
```

---

### Why this matters

* Automatically fetches all posts
* Sends them to template as `posts`
* Sorted newest → oldest

---

### 2. Detail View (Single Post)

```python id="hx4b0x"
class PostDetailView(DetailView):
    model = Post
```

URL:

```python id="0u8m6j"
path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')
```

---

### Why `<int:pk>`?

👉 Django uses primary key to fetch object automatically

---

### 3. get_absolute_url (IMPORTANT)

```python id="o5tx0k"
def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
```

---

### Why needed

After create/update:
👉 Django needs to know **where to redirect**

Without this:
❌ Error OR no redirect

---

### 4. Create View

```python id="0uqj9z"
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

### Why override `form_valid`

👉 Author is not in form
👉 You manually attach logged-in user

---

### 5. LoginRequiredMixin

```python id="w6rg6c"
LoginRequiredMixin
```

👉 Prevents anonymous users from:

* creating posts
* updating
* deleting

---

### 6. Update View

```python id="v2o7pq"
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

### Why `UserPassesTestMixin`

👉 Only author should edit post

```python id="h3s4pw"
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

---

### 7. Delete View

```python id="a9g7kl"
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
```

---

### Why `success_url`

👉 After delete, object no longer exists
👉 So redirect manually

---

### 8. Templates

#### Detail page

```html id="6m8h3a"
{{ object.title }}
{{ object.content }}
```

👉 Django sends object automatically

---

#### Show update/delete only to author

```html id="t2r7qp"
{% if object.author == user %}
    <a href="{% url 'post-update' object.id %}">Update</a>
    <a href="{% url 'post-delete' object.id %}">Delete</a>
{% endif %}
```

---

#### Delete confirmation

```html id="l8u3mw"
<form method="POST">
    {% csrf_token %}
    <button type="submit">Yes, Delete</button>
</form>
```

---

### 9. Form Template (Create/Update shared)

```html id="4cx7hk"
{{ form|crispy }}
```

👉 Django auto-uses:

```id="y2t4vl"
post_form.html
```

---

### 10. Flow (important)

#### Create

1. User submits form
2. `form_valid()` runs
3. Author assigned
4. Redirect → `get_absolute_url()`

---

#### Update

1. Existing object loaded
2. User edits
3. Saved
4. Redirect → same post

---

#### Delete

1. Confirmation page
2. POST submit
3. Object deleted
4. Redirect → `success_url`

---

### Common mistakes

* ❌ duplicate URL paths
* ❌ forgetting `get_absolute_url`
* ❌ forgetting `LoginRequiredMixin`
* ❌ forgetting `test_func` → anyone can edit/delete
* ❌ not setting author in `form_valid`

---

### Core understanding (this is the real takeaway)

* CBVs = reusable patterns
* Mixins = permission control
* `form_valid` = inject custom logic
* `get_absolute_url` = redirect control

---



## Part 11 — Pagination + User Posts

### 0. Goal

* Split posts into multiple pages
* Show posts by specific user
* Handle pagination UI

---

### 1. Load Data from JSON (optional setup)

```python
import json
from blog.models import Post

with open('posts.json') as f:
    posts_json = json.load(f)

for post in posts_json:
    Post.objects.create(
        title=post['title'],
        content=post['content'],
        author_id=post['user_id']
    )
```

---

### Why this matters

👉 Quickly populate database for testing pagination

---

### 2. Pagination Concept (core idea)

```python
from django.core.paginator import Paginator

posts = ['1','2','3','4','5']
p = Paginator(posts, 2)
```

* 2 items per page
* total pages = 3

---

### Key attributes

* `p.num_pages` → total pages
* `p.page(n)` → specific page
* `has_next()` / `has_previous()`

---

### 3. Enable Pagination in CBV

```python
class PostListView(ListView):
    model = Post
    paginate_by = 5
```

👉 That’s it — Django handles pagination automatically

---

### 4. Pagination Template Logic

```html
{% if is_paginated %}

    {% if page_obj.has_previous %}
        <a href="?page=1">First</a>
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}

    {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
            <a class="btn btn-info" href="?page={{ num }}">{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
            <a class="btn btn-outline-info" href="?page={{ num }}">{{ num }}</a>
        {% endif %}
    {% endfor %}

    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
    {% endif %}

{% endif %}
```

---

### ❌ Your mistake (IMPORTANT)

You wrote:

```html
{% if page.obj.number == num %}
```

👉 Wrong variable

✔ Fix:

```html
{% if page_obj.number == num %}
```

---

### 5. Link to User Posts

```html
<a href="{% url 'user-posts' post.author.username %}">
    {{ post.author }}
</a>
```

---

### 6. UserPostListView

```python
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
```

---

### Why override `get_queryset`

👉 Default = all posts
👉 We want = posts of specific user

---

### 7. URL

```python
path('user/<str:username>/', UserPostListView.as_view(), name='user-posts')
```

---

### Why `<str:username>`

👉 URL example:

```text
/user/ArnavF/
```

Django passes:

```python
self.kwargs['username']
```

---

### 8. User Posts Template

```html
<h1>Posts by {{ view.kwargs.username }} ({{ page_obj.paginator.count }})</h1>
```

---

### Why `page_obj.paginator.count`

👉 total posts count (not just current page)

---

### 9. Flow (important)

1. User clicks author name
2. URL → `/user/ArnavF/`
3. `get_queryset()` filters posts
4. Pagination applies
5. Template shows paginated posts

---

### Common mistakes (you hit one already)

* ❌ `page.obj.number` → typo
* ❌ forgetting `paginate_by`
* ❌ not overriding `get_queryset`
* ❌ wrong field name (`date-posted`)

---

### Core understanding

* Pagination = handled by CBV automatically
* `page_obj` = current page data
* `paginator` = metadata (total pages, count)
* `get_queryset()` = customize data

---

## Part 12 - Email and password reset
- we will be learning how to use email to allow users to reset there passwords
- so django has built in functionality that genreate a secure token - only a specific user can reset there password
- then we will see how we can send email at django that has instructions for userr to reset there password

# Part 12 - Email and Password Reset

## What We Built
Full password reset flow using Django's built-in auth views + real Gmail SMTP.

---

## Flow
User clicks "Forgot Password?" → fills email → gets email → clicks link → sets new password → done.

---

## 1. URLs (django_project/django_project/urls.py)
Added 4 paths using Django's built-in auth views:

path('password-reset/', PasswordResetView → password_reset.html)
path('password-reset/done/', PasswordResetDoneView → password_reset_done.html)
path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView → password_reset_confirm.html)
path('password-reset-complete/', PasswordResetCompleteView → password_reset_complete.html)

---

## 2. Templates (users/templates/users/)
4 templates created:

- password_reset.html → form to enter email
- password_reset_done.html → "email has been sent" message
- password_reset_confirm.html → form to enter new password
- password_reset_complete.html → "password has been set" + login link

Also added "Forgot Password?" link in login.html:
<a href="{% url 'password_reset' %}">Forgot Password?</a>

---

## 3. Gmail App Password Setup
1. Go to myaccount.google.com → Security
2. 2-Step Verification must be ON
3. App Passwords → name it "Django" → Create
4. Copy the 16-character password (shown only once, don't close without copying)
5. DON'T DELETE IT or you have to regenerate and update .env

My Gmail: arnavfating09@gmail.com

---

## 4. .env (django_project/.env — sits next to manage.py)
EMAIL_USER=arnavfating09@gmail.com
EMAIL_PASS=vlozpsqskeclodxw

IMPORTANT:
- .env is in .gitignore — never push to GitHub
- Don't delete the Django app password from Google or this breaks

---

## 5. settings.py Changes

### Top of file:
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

### Bottom of file:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

---

## 6. Install Dependency
pip install python-dotenv

---

## Important Gotchas Learned
- Password reset email only sends if submitted email matches a registered user in DB.
  Django silently redirects to done/ either way (security by design).
- For local testing only, use console backend (prints email in terminal):
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
- Always restart runserver after changing settings.py
- Registered user email in DB must match the email you test with.
  Changed via Django admin panel → Users → ArnavF → Email address.



#### ~`*here is you can do:*`



# Django Password Reset + Gmail SMTP Setup

## 1. URLs Required (django_project/urls.py)
Add all 4 password reset paths:
- password-reset/
- password-reset/done/
- password-reset-confirm/<uidb64>/<token>/
- password-reset-complete/

## 2. Templates Required (users/templates/users/)
- password_reset.html
- password_reset_done.html
- password_reset_confirm.html
- password_reset_complete.html

## 3. Gmail Setup
1. Go to myaccount.google.com → Security
2. Make sure 2-Step Verification is ON
3. Go to App Passwords → type any name (e.g. "Django") → Create
4. Copy the 16-character password shown (only shown once)

## 4. .env file (same folder as manage.py)
EMAIL_USER=youremail@gmail.com
EMAIL_PASS=yoursixteencharpassword

## 5. settings.py
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

## 6. Install python-dotenv if not already
pip install python-dotenv

## Important Notes
- For local testing only, use console backend instead of smtp:
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
  (email prints in terminal instead of actually sending)

- Password reset email only sends if the submitted email
  matches a registered user in the database.

- Never commit .env to GitHub. Add it to .gitignore.
------

----
#### Here's your note tailored to your project:

# Django Password Reset + Gmail SMTP Setup
## Project: Corey Schafer Django (django_project)

## 1. URLs (django_project/django_project/urls.py)
All 4 paths already added and working.

## 2. Templates (users/templates/users/)
All 4 templates already created and working.

## 3. Gmail App Password
- Gmail: arnavfating09@gmail.com
- Go to myaccount.google.com → Security → App Passwords
- Created app named "Django"
- DON'T DELETE IT or you'll have to regenerate and update .env

## 4. .env file (django_project/.env — next to manage.py)
EMAIL_USER=arnavfating09@gmail.com
EMAIL_PASS=vlozpsqskeclodxw

## 5. settings.py changes made
- Added at top:
  from dotenv import load_dotenv
  load_dotenv()

- Added at bottom:
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

## 6. .gitignore
Make sure .env is in .gitignore — never push it to GitHub.

## Testing
- Registered user email in DB: arnavfating09@gmail.com (changed via admin panel)
- Reset flow tested and working end to end.


------
------
------
# Secret Leaked on GitHub - What To Do

## If repo is PRIVATE
1. Immediately add .gitignore with .env in it
2. Never make repo public without cleaning history first

## If repo is PUBLIC (emergency steps)
1. Immediately go to Google → App Passwords → DELETE the leaked password
   (This invalidates it instantly — anyone who copied it can no longer use it)
2. Generate a new App Password
3. Update .env with new password
4. Add .gitignore (see below)
5. Remove .env from git history (see below)

---

## .gitignore (create next to manage.py)
.env
*.pyc
__pycache__/
db.sqlite3
media/

---

## Remove .env from entire git history
Run these commands one by one:

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all

git push origin --force --all

WARNING: This rewrites history. If others are working on the repo, 
tell them to re-clone it after this.

---

## Key Lesson
.env should NEVER be committed in the first place.
Always create .gitignore before your first commit in any new project.
------
------
------
------
------

# Deployment - Django Blog on Render + Neon PostgreSQL
## Project: CoreyShafer_django_project
## Live URL: https://arnav-coreyms-django-blog.onrender.com

---

## Architecture (How It Works)
```
Your VS Code (Local)
      ↓ git push
GitHub (CoreyShafer_django_project) — PUBLIC repo
      ↓ auto-deploy
Render (Web Server - runs gunicorn)
      ↓ connects to
Neon (PostgreSQL Database)
```

- **Code** lives on GitHub
- **Server** runs on Render (gunicorn serves the Django app)
- **Database** lives on Neon (PostgreSQL)
- **Static files** (CSS/JS) served by whitenoise directly from Render

---

## How HTTPS Works
Render automatically provides SSL (HTTPS) for free on all deployments.
You don't configure anything — Render handles the certificate.
That's why the URL starts with `https://` not `http://`.

---

## Accounts Used
- GitHub: Arnav-Naive (repo: CoreyShafer_django_project) — PUBLIC
- Render: arnavfating09@gmail.com → https://dashboard.render.com
- Neon: arnavfating09@gmail.com → https://console.neon.tech

---

## Packages Installed for Deployment
```
pip install gunicorn          # production web server
pip install whitenoise        # serves static files in production
pip install dj-database-url   # parses DATABASE_URL string
pip install psycopg2-binary   # PostgreSQL adapter for Django
```

---

## Settings.py Changes Made

### 1. Imports at top
```python
import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
```

### 2. ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['arnav-coreyms-django-blog.onrender.com']
```

### 3. MIDDLEWARE — whitenoise added after SecurityMiddleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # added
    ...
]
```

### 4. DATABASES — handles both SQLite (local) and PostgreSQL (production)
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}
```
- If DATABASE_URL exists → uses Neon PostgreSQL
- If DATABASE_URL not set → falls back to SQLite

### 5. Static files
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## .env File (django_project/.env — next to manage.py)
```
SECRET_KEY=django-insecure-r0+o0dm075u)7mgyf)!-o3uolk%z362%=y_ypz)qdwau&mb8)+
EMAIL_USER=arnavfating09@gmail.com
EMAIL_PASS=vlozpsqskeclodxw
# DATABASE_URL=postgresql://neondb_owner:npg_r1GhJ9nHOBkA@ep-muddy-truth-anz9qri2.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
```
DATABASE_URL is commented out locally → uses SQLite
Render has DATABASE_URL set as environment variable → uses Neon

---

## Render Configuration
- **Service name:** Arnav_CoreyMS_django-blog
- **Root Directory:** django_project
- **Build Command:** pip install -r requirements.txt && python manage.py collectstatic --noinput
- **Start Command:** gunicorn django_project.wsgi
- **Instance Type:** Free

### Environment Variables set on Render dashboard:
```
SECRET_KEY=...
EMAIL_USER=arnavfating09@gmail.com
EMAIL_PASS=vlozpsqskeclodxw
DATABASE_URL=postgresql://neondb_owner:npg_r1GhJ9nHOBkA@ep-muddy-truth-anz9qri2.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
```

---

## Neon PostgreSQL
- Project: django-blog
- Region: AWS US East 1
- Connection string in .env as DATABASE_URL
- View data: https://console.neon.tech → SQL Editor
```sql
SELECT * FROM auth_user;
SELECT * FROM blog_post;
```

---

## How to Deploy Code Changes
Every time you change code locally:
```
git add .
git commit -m "your message"
git push
```
Render auto-deploys on every push. No manual steps needed.

---

## How to Create Superuser on Production DB
Since Render Shell is paid only, do this locally:
1. Uncomment DATABASE_URL in .env
2. Run: python manage.py createsuperuser
3. Comment DATABASE_URL back out

---

## Free Tier Limits
- Render: 750 hours/month, 100GB bandwidth, spins down after 15 min inactivity (50 sec cold start)
- Neon: 0.5GB storage, scales to zero when inactive
- No credits system — just these limits

---

## Important Notes
- Render free tier = 1 web service only
- When deploying MediScan/Job Tracker → delete this service first, deploy that instead
- .env is in .gitignore — never pushed to GitHub
- Render reads its own environment variables, NOT your .env file
- Never make repo private without removing sensitive history first


----------------------------------------------------
------------------------------------------------
----------------------------------------
# for public

# Deployment - Django App on Render + Neon PostgreSQL

---

## Architecture (How It Works)
```
Your VS Code (Local)
      ↓ git push
GitHub (your repo) — must be PUBLIC
      ↓ auto-deploy
Render (Web Server - runs gunicorn)
      ↓ connects to
Neon (PostgreSQL Database)
```

- **Code** lives on GitHub
- **Server** runs on Render (gunicorn serves the Django app)
- **Database** lives on Neon (PostgreSQL)
- **Static files** (CSS/JS) served by whitenoise directly from Render

---

## How HTTPS Works
Render automatically provides SSL (HTTPS) for free on all deployments.
You don't configure anything — Render handles the certificate.
That's why the URL starts with `https://` not `http://`.

---

## Accounts Required
- GitHub — repo must be PUBLIC
- Render — https://dashboard.render.com (free, no card needed)
- Neon — https://console.neon.tech (free, no card needed)

---

## Step 1: Packages to Install
```
pip install gunicorn          # production web server
pip install whitenoise        # serves static files in production
pip install dj-database-url   # parses DATABASE_URL string
pip install psycopg2-binary   # PostgreSQL adapter for Django
pip freeze > requirements.txt
```

---

## Step 2: Settings.py Changes

### Imports at top
```python
import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
```

### ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['your-app-name.onrender.com']
```

### MIDDLEWARE — add whitenoise after SecurityMiddleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add this
    ...
]
```

### DATABASES — handles both SQLite (local) and PostgreSQL (production)
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}
```
- DATABASE_URL set → uses Neon PostgreSQL
- DATABASE_URL not set → falls back to SQLite

### Static files
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Step 3: .env File (next to manage.py)
```
SECRET_KEY=your_secret_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
# DATABASE_URL=your_neon_connection_string
```
- DATABASE_URL commented out locally → uses SQLite
- Render has DATABASE_URL set as environment variable → uses Neon

---

## Step 4: .gitignore (next to manage.py)
```
.env
*.pyc
__pycache__/
db.sqlite3
media/
.venv/
venv/
.vscode/
```

---

## Step 5: Neon Setup
1. Go to https://console.neon.tech → create project
2. Copy the connection string (looks like):
   `postgresql://user:password@host/dbname?sslmode=require`
3. Add to .env as DATABASE_URL (uncommented) and run:
```
   python manage.py migrate
```
4. Comment DATABASE_URL back out in .env

---

## Step 6: Render Setup
1. Go to https://dashboard.render.com → New Web Service
2. Connect your GitHub repo (Public Git Repository → paste URL)
3. Fill in:
   - **Root Directory:** your_project_folder (where manage.py is)
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn your_project.wsgi`
   - **Instance Type:** Free
4. Add Environment Variables:
```
   SECRET_KEY=your_secret_key
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   DATABASE_URL=your_neon_connection_string
```
5. Click Deploy

---

## Step 7: Create Production Superuser
Since Render Shell is paid only, do this locally:
1. Uncomment DATABASE_URL in .env
2. Run: `python manage.py createsuperuser`
3. Comment DATABASE_URL back out

---

## How to Deploy Code Changes
```
git add .
git commit -m "your message"
git push
```
Render auto-deploys on every push automatically.

---

## Viewing Production Database
Go to https://console.neon.tech → SQL Editor:
```sql
SELECT * FROM auth_user;
SELECT * FROM your_app_table;
```

---

## Free Tier Limits
| Service | Limit |
|---------|-------|
| Render | 750 hours/month, 100GB bandwidth, spins down after 15 min inactivity |
| Neon | 0.5GB storage, scales to zero when inactive |

First request after spin down takes ~50 seconds. After that it's fast.

---

## Important Notes
- Render free tier = 1 web service only
- Render reads its own environment variables, NOT your .env file
- .env must be in .gitignore — never push secrets to GitHub
- Repo must be PUBLIC for Render free tier (or use Public Git Repository URL)
- HTTPS is automatic — Render handles SSL certificates

# Part 13 - Using AWS S3 for File Uploads
1 . need account with AmazonWebServices - sign up
2. Find Services
    Type: S3 (simple storage service)

3. create bucket
.
.
.
 then he created user security credintials
    User - django_user
    Access key ID - AKIAIARCV3....
    Secret access key - ********

    somthing like that

    then opened .bash_profile in his submilme text ide 
`   export AWS_ACCESS_KEY_ID="AKIAIARCV3...."  `
`   export AWS_SECRET_ACCESS_KEY="hXodDKfnKNIUDhBD...."    `
`   export AWS_STORAGE_BUCKET_NAME="djangi-blog-files"     `
.
.
.
lets now change the django code to use S3 insted of the local file system
install packeages- boto3(aws django packages),django-storages 

then he made change sto syttings.py file
`       INSTALLED APPS = ['storages ']      `
`    AWS_ACCESS_KEY_ID=os.envirn.get(AWS_ACCESS_KEY_ID)         `
`          AWS_SECRET_ACCESS_KEY=os.envirn.get(AWS_SECRET_ACCESS_KEY)   `
`AWS_STORAGE_BUCKET_NAME=os.envirn.get(AWS_STORAGE_BUCKET_NAME)`

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'sotrages.backends.s3boto3.s3...'

then he commented out/removed this from models.py (users)
def save(self, *args, **kwargs): 
        super().save(*args, **kwargs) 

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

then he did somthis drage the images to asw

then when we opene the image in new tab it compes from https://djnago-blig-files.s3-us-west-2.amazon.com/profile_pic/....


what just happed here i just dont get it, is it cloud or smthing... help me with this and tell how to i do this too / is it even important to have to this knowledge no a days and if so tell me,
give me step by step way...