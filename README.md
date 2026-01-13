# Social Network - Django Project

A Twitter-like social network web application built with Django, allowing users to create posts, follow other users, like posts, and view personalized feeds.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Database Models](#database-models)
- [URL Routes](#url-routes)
- [Key Functionality](#key-functionality)

## 🎯 Project Overview

This is a full-stack web application that implements a social networking platform where users can:
- Create and manage user accounts
- Post messages (up to 280 characters)
- Follow/unfollow other users
- Like/unlike posts
- Edit their own posts
- View personalized feeds (All Posts, Following feed, User profiles)

## ✨ Features

### User Authentication
- User registration with username, email, and password
- Login and logout functionality
- Session management

### Posts
- Create new posts (max 280 characters)
- Edit own posts (inline editing with JavaScript)
- View all posts with pagination (10 posts per page)
- Posts ordered by timestamp (newest first)

### Social Features
- Follow/unfollow other users
- View followers and following counts
- Like/unlike posts (with real-time count updates)
- View posts from users you follow

### User Profiles
- View any user's profile page
- See all posts by a specific user
- Follow/unfollow buttons (only for other users)
- Follower and following statistics

### UI/UX
- Responsive Bootstrap-based design
- Real-time like updates (no page refresh)
- Inline post editing
- Pagination for better performance
- Clean, modern interface

## 📁 Project Structure

```
project4/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── network/                 # Main application directory
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models (User, Post, Follow)
│   ├── views.py            # View functions (business logic)
│   ├── urls.py             # URL routing
│   ├── tests.py            # Unit tests
│   ├── migrations/         # Database migrations
│   │   ├── 0001_initial.py
│   │   └── 0002_post_follow.py
│   ├── static/
│   │   └── network/
│   │       ├── styles.css  # Custom CSS
│   │       └── script.js   # JavaScript for AJAX functionality
│   └── templates/
│       └── network/
│           ├── layout.html      # Base template
│           ├── index.html        # All posts page
│           ├── profile.html      # User profile page
│           ├── following.html    # Following feed page
│           ├── login.html        # Login page
│           ├── register.html     # Registration page
│           └── error.html        # Error page
└── project4/               # Django project settings
    ├── __init__.py
    ├── settings.py        # Django settings
    ├── urls.py            # Root URL configuration
    ├── wsgi.py            # WSGI configuration
    └── asgi.py            # ASGI configuration
```

## 🛠 Technology Stack

- **Backend**: Django 3.0.2 (Python web framework)
- **Database**: SQLite3
- **Frontend**: 
  - HTML5 with Django Templates
  - Bootstrap 4.4.1 (CSS framework)
  - Vanilla JavaScript (for AJAX requests)
- **Authentication**: Django's built-in authentication system

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd project4
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Django**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000`

## 📖 Usage

### Getting Started

1. **Register a new account**
   - Click "Register" in the navigation bar
   - Enter username, email, and password
   - Confirm password and submit

2. **Login**
   - Click "Log In" in the navigation bar
   - Enter your credentials

3. **Create a post**
   - On the "All Posts" page, write your post in the textarea
   - Click "Post" to publish (max 280 characters)

4. **Follow users**
   - Click on a username to view their profile
   - Click "Follow" to follow them
   - Click "Unfollow" to stop following

5. **Like posts**
   - Click the heart icon (🤍) to like a post
   - Click again (❤️) to unlike
   - Like count updates in real-time

6. **Edit posts**
   - Click "Edit" on your own posts
   - Modify the content in the textarea
   - Click "Save" or "Cancel"

7. **View feeds**
   - **All Posts**: See all posts from all users
   - **Following**: See posts only from users you follow
   - **Profile**: See all posts from a specific user

## 🗄 Database Models

### User Model
- Extends Django's `AbstractUser`
- No additional fields (uses default Django user fields)

### Post Model
```python
- author: ForeignKey to User
- content: TextField (max 280 characters)
- timestamp: DateTimeField (auto-created)
- likes: ManyToManyField to User
- Methods:
  - like_count(): Returns number of likes
```

### Follow Model
```python
- follower: ForeignKey to User (who follows)
- following: ForeignKey to User (who is followed)
- created_at: DateTimeField (auto-created)
- Unique constraint: (follower, following) - prevents duplicate follows
```

## 🔗 URL Routes

| URL Pattern | View Function | Description |
|------------|---------------|-------------|
| `/` | `index` | All posts page |
| `/login` | `login_view` | User login |
| `/logout` | `logout_view` | User logout |
| `/register` | `register` | User registration |
| `/create` | `create_post` | Create new post (POST only) |
| `/profile/<username>` | `profile` | User profile page |
| `/follow/<username>` | `follow` | Follow/unfollow user (POST only) |
| `/following` | `following` | Posts from followed users |
| `/edit/<post_id>` | `edit_post` | Edit post (PUT, JSON API) |
| `/like/<post_id>` | `toggle_like` | Like/unlike post (POST, JSON API) |

## 🔑 Key Functionality

### Authentication & Authorization
- Uses Django's built-in authentication system
- `@login_required` decorator protects certain views
- Users can only edit their own posts
- Users cannot follow themselves

### Pagination
- All post listings use pagination (10 posts per page)
- Implemented using Django's `Paginator` class
- Navigation: First, Previous, Next, Last

### AJAX Functionality
- **Edit Post**: Inline editing without page refresh
  - PUT request to `/edit/<post_id>`
  - Returns JSON response
- **Like/Unlike**: Real-time like updates
  - POST request to `/like/<post_id>`
  - Returns JSON with liked status and count

### Security Features
- CSRF protection (except for AJAX endpoints using `@csrf_exempt`)
- Password validation on registration
- Authorization checks (users can only edit own posts)
- SQL injection protection (Django ORM)

## 🎨 Frontend Architecture

### Templates
- **Base Template** (`layout.html`): Contains navigation bar and common structure
- **Child Templates**: Extend base template using `{% extends %}`
- **Template Inheritance**: Reduces code duplication

### JavaScript (`script.js`)
- Handles client-side interactions:
  - Edit button click → converts content to textarea
  - Save button → sends PUT request to server
  - Like button → sends POST request, updates UI
- Uses `fetch()` API for AJAX requests
- Updates DOM without page refresh

### CSS (`styles.css`)
- Custom styles for like buttons
- Removes default button styling for cleaner look

## 🔧 Development Notes

### Custom User Model
- Uses `AUTH_USER_MODEL = "network.User"` in settings
- Allows for future customization of user model

### Database Migrations
- Initial migration creates User and Post models
- Second migration adds Follow model

### Static Files
- CSS and JavaScript served from `network/static/network/`
- Bootstrap CDN used for main styling

## 📝 Future Enhancements (Potential)

- Comments on posts
- Image uploads
- Direct messaging
- Notifications
- Search functionality
- Hashtags and mentions
- User avatars
- Post deletion
- Email verification

## 📄 License

This project is part of CS50's Web Programming course.

## 👤 Author

Created as part of CS50W Project 4 - Network
