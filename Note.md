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
