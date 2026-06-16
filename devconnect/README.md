# DevConnect - Developer Community Platform

DevConnect is a full-stack social platform built using Django where developers can create profiles, publish posts, interact through comments, follow users, bookmark content, and discover similar posts.

## Features

- User Authentication
- User Profiles
- Image Uploads
- Create, Update and Delete Posts
- Tags using django-taggit
- Comments System
- Email Sharing
- Search Functionality
- Similar Post Recommendations
- Bookmark Posts
- Follow/Unfollow Users
- Password Reset
- Rich Text Editor
- Responsive Bootstrap UI

## Tech Stack

- Python
- Django
- SQLite
- Bootstrap
- HTML
- CSS
- Pillow
- django-taggit
- CKEditor

## Installation

```bash
git clone <repository-url>

cd devconnect-django

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```