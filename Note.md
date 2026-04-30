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



## Part 11 - Pagination

- paginate our site ->so that our post are brokenup into diff pages
- how to create page for specific user's post


    - pagination working on website
    - diff ways in which u create the links and handel the logic for those in your application
    - how to create new list views with coustom  filtered queries
    - and created a useful route for post  written by specific user


    1. (.venv) (base) PS C:\Arnav-Projects\Learning\Corey Schafer Django\django_project> python .\manage.py shell                                                               
14 objects imported automatically (use -v 2 for details).     

Ctrl click to launch VS Code Native REPL
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import json
>>> from blog.models import Post
>>> with open('posts.json') as f:
...     posts_json = json.load(f)
... 
>>> 
>>> for post in posts_json:
...     post = Post(title=post['title'],content=post['content'], author_id=post['user_id'])
...     post.save()
... 

>>> exit()
now exiting InteractiveConsole...

2. pagination

>>> from django.core.paginator import Paginator
>>> post = ['1']
KeyboardInterrupt
>>>                                            
>>> post = ['1', '2', '3', '4', '5'] 
>>> p = Paginator(post, 2)
>>> p.num_pages
3
>>> for page in p.page_range:
...     print(page)
... 
1
2
3
>>> p1 = p.page(1)
>>> 
>>> p1
<Page 1 of 3>
>>> p1.number
1
>>> p1.object_list
['1', '2']
>>> p1.has_previous() 
False
>>> p1.has_next()
True
>>> p1.next_page_number()
2
>>> exit()

3. paginaton logic in home.html
{% if is_paginated %}
    
        {% if page_obj.has_previous %}
            <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}
            
            {% for num in page_obj.paginator.page_range %}
                {% if page.obj.number == num %}
                    <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %} 
                    <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
                {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
                <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
                <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">last</a>
            {% endif %}

    {% endif %}

4. 
- views/
- class UserPostListViews(ListView):
.
.
    def get_queryset(self):
        .
        .
5. urls.py

6. user_post.html
