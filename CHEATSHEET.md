# Social Network - Quick Reference Cheatsheet

## 🚀 Quick Start Commands

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

## 📂 File Structure Quick Reference

```
project4/
├── manage.py                    # Django CLI
├── network/
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── urls.py                 # URL routing
│   ├── static/network/
│   │   ├── script.js           # AJAX handlers
│   │   └── styles.css          # Custom styles
│   └── templates/network/      # HTML templates
└── project4/
    └── settings.py             # Django settings
```

## 🗄️ Database Models

### User
```python
# Extends AbstractUser
# Fields: username, email, password, etc. (Django default)
```

### Post
```python
author = ForeignKey(User)
content = TextField(max_length=280)
timestamp = DateTimeField(auto_now_add=True)
likes = ManyToManyField(User)

# Methods
post.like_count()  # Returns number of likes
```

### Follow
```python
follower = ForeignKey(User)      # Who follows
following = ForeignKey(User)     # Who is followed
created_at = DateTimeField(auto_now_add=True)

# Unique constraint: (follower, following)
```

## 🔗 URL Patterns

```python
# network/urls.py
""                    → index()           # All posts
"login"               → login_view()      # Login
"logout"              → logout_view()     # Logout
"register"            → register()        # Register
"create"               → create_post()     # Create post (POST)
"profile/<username>"   → profile()        # User profile
"follow/<username>"    → follow()         # Follow/unfollow (POST)
"following"            → following()      # Following feed
"edit/<post_id>"       → edit_post()      # Edit post (PUT, JSON)
"like/<post_id>"       → toggle_like()    # Like/unlike (POST, JSON)
```

## 🎯 View Functions Reference

### `index(request)`
- **Purpose**: Display all posts
- **Method**: GET
- **Pagination**: 10 posts per page
- **Template**: `index.html`

### `create_post(request)`
- **Purpose**: Create new post
- **Method**: POST
- **Auth**: `@login_required`
- **Redirect**: Back to index

### `profile(request, username)`
- **Purpose**: Show user profile
- **Method**: GET
- **Context**: 
  - `profile_user`
  - `page_obj` (paginated posts)
  - `is_following`
  - `followers_count`
  - `following_count`

### `follow(request, username)`
- **Purpose**: Toggle follow/unfollow
- **Method**: POST
- **Auth**: `@login_required`
- **Logic**: Toggle (create if not exists, delete if exists)

### `following(request)`
- **Purpose**: Show posts from followed users
- **Method**: GET
- **Auth**: `@login_required`
- **Template**: `following.html`

### `edit_post(request, post_id)`
- **Purpose**: Edit post content
- **Method**: PUT
- **Auth**: `@login_required`
- **Response**: JSON
- **Security**: Only author can edit

### `toggle_like(request, post_id)`
- **Purpose**: Like/unlike post
- **Method**: POST
- **Auth**: `@login_required`
- **Response**: JSON `{liked: bool, like_count: int}`

### `login_view(request)`
- **Purpose**: User authentication
- **Method**: GET (form) / POST (submit)

### `logout_view(request)`
- **Purpose**: Logout user
- **Redirect**: Index page

### `register(request)`
- **Purpose**: Create new user account
- **Method**: GET (form) / POST (submit)
- **Validation**: Password confirmation

## 🔐 Authentication Decorators

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # Only authenticated users can access
    pass
```

## 📊 Django ORM Queries

### Post Queries
```python
# Get all posts
Post.objects.all()

# Get posts by user
Post.objects.filter(author=user)

# Get posts from multiple users
Post.objects.filter(author__in=user_list)

# Get single post
Post.objects.get(pk=post_id)

# Order by timestamp (newest first)
Post.objects.all().order_by('-timestamp')
```

### Follow Queries
```python
# Check if user A follows user B
Follow.objects.filter(follower=user_a, following=user_b).exists()

# Get all users that user A follows
Follow.objects.filter(follower=user_a).values_list('following', flat=True)

# Count followers
Follow.objects.filter(following=user).count()

# Count following
Follow.objects.filter(follower=user).count()

# Create follow relationship
Follow.objects.create(follower=user_a, following=user_b)

# Delete follow relationship
Follow.objects.filter(follower=user_a, following=user_b).delete()
```

### Like Queries
```python
# Check if user liked post
user in post.likes.all()

# Add like
post.likes.add(user)

# Remove like
post.likes.remove(user)

# Count likes
post.likes.count()
# or
post.like_count()  # Using model method
```

### User Queries
```python
# Get user by username
User.objects.get(username=username)

# Get authenticated user
request.user

# Check if user is authenticated
request.user.is_authenticated
```

## 📄 Pagination

```python
from django.core.paginator import Paginator

# Create paginator (10 items per page)
paginator = Paginator(posts, 10)

# Get page number from request
page_number = request.GET.get('page')

# Get page object
page_obj = paginator.get_page(page_number)

# In template:
# page_obj.has_previous
# page_obj.has_next
# page_obj.previous_page_number
# page_obj.next_page_number
# page_obj.number
# page_obj.paginator.num_pages
```

## 🌐 Template Tags & Filters

### Common Template Tags
```django
{% extends "network/layout.html" %}
{% block body %}...{% endblock %}
{% load static %}
{% url 'view_name' %}
{% url 'profile' username %}
{% csrf_token %}
{% if user.is_authenticated %}...{% endif %}
{% for post in page_obj %}...{% endfor %}
{% empty %}...{% endfor %}
```

### Template Filters
```django
{{ post.timestamp|date:"M d, Y, g:i a" }}
{{ post.content|truncatewords:50 }}
```

### Static Files
```django
{% load static %}
<link href="{% static 'network/styles.css' %}" rel="stylesheet">
<script src="{% static 'network/script.js' %}"></script>
```

## 🔄 AJAX Requests (JavaScript)

### Edit Post
```javascript
fetch(`/edit/${postId}`, {
    method: 'PUT',
    body: JSON.stringify({ content: newContent })
})
.then(response => response.json())
.then(data => {
    // Handle response
});
```

### Toggle Like
```javascript
fetch(`/like/${postId}`, {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    // Update UI with data.liked and data.like_count
});
```

## 🎨 Bootstrap Classes Used

```html
<!-- Layout -->
<div class="container mt-4">
<div class="card mb-3">
<div class="card-body">

<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-sm btn-outline-primary">Small Outline</button>
<button class="btn btn-link">Link Style</button>

<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
<ul class="navbar-nav mr-auto">
<li class="nav-item">
<a class="nav-link" href="...">Link</a>

<!-- Pagination -->
<nav aria-label="Page navigation">
<ul class="pagination justify-content-center">
<li class="page-item">
<a class="page-link" href="...">Link</a>

<!-- Forms -->
<form>
<div class="form-group">
<textarea class="form-control" rows="3"></textarea>
```

## 🔒 Security Best Practices

```python
# CSRF Protection (for forms)
{% csrf_token %}

# CSRF Exempt (for AJAX endpoints only)
@csrf_exempt
@login_required
def api_view(request):
    pass

# Authorization Check
if post.author != request.user:
    return JsonResponse({"error": "Not authorized"}, status=403)

# Prevent self-follow
if user_to_follow != request.user:
    # Allow follow
```

## 📝 Common Patterns

### Redirect After Action
```python
return HttpResponseRedirect(reverse("index"))
return HttpResponseRedirect(reverse("profile", args=[username]))
```

### JSON Response
```python
return JsonResponse({"message": "Success", "data": value}, status=200)
return JsonResponse({"error": "Error message"}, status=400)
```

### Error Handling
```python
try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    return render(request, "network/error.html", {
        "message": "User not found."
    })
```

### Check Authentication in Template
```django
{% if user.is_authenticated %}
    <!-- Authenticated user content -->
{% else %}
    <!-- Guest content -->
{% endif %}
```

### Check Ownership
```django
{% if user.is_authenticated and post.author == user %}
    <!-- Owner-only content -->
{% endif %}
```

## 🐛 Debugging Tips

```python
# Print to console
print(variable)

# Django shell
python manage.py shell
>>> from network.models import Post, User
>>> Post.objects.all()

# Check migrations
python manage.py showmigrations

# Reset database (WARNING: deletes all data)
python manage.py flush
```

## 📦 Key Imports

```python
# Views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

# Models
from django.contrib.auth.models import AbstractUser
from django.db import models
```

## 🎯 Quick Checklist for New Features

- [ ] Create/update model in `models.py`
- [ ] Run `makemigrations` and `migrate`
- [ ] Create view function in `views.py`
- [ ] Add URL pattern in `urls.py`
- [ ] Create/update template in `templates/network/`
- [ ] Add JavaScript if needed in `script.js`
- [ ] Test authentication requirements
- [ ] Test authorization (who can access)
- [ ] Add error handling
- [ ] Test pagination if listing items

## 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Template not found | Check `TEMPLATES` in `settings.py` |
| Static files not loading | Run `python manage.py collectstatic` (production) |
| CSRF error | Add `{% csrf_token %}` to form |
| Migration error | Delete `migrations/` folder (except `__init__.py`) and re-migrate |
| User model error | Check `AUTH_USER_MODEL` in `settings.py` |
| 404 error | Check URL patterns in `urls.py` |
| 403 error | Check `@login_required` and authorization |

## 📚 Django Concepts Used

- **Models**: Database schema definition
- **Views**: Request handlers (business logic)
- **Templates**: HTML with Django template language
- **URLs**: URL routing
- **Forms**: HTML form handling
- **Authentication**: User login/logout
- **Pagination**: Split content into pages
- **AJAX**: Asynchronous JavaScript requests
- **JSON**: Data exchange format
- **Middleware**: Request/response processing
- **Static Files**: CSS, JavaScript, images
