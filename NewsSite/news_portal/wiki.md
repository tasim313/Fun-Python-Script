# Project Summary
The Django News Portal is a feature-rich web application designed for publishing and managing news articles in Bengali. It aims to provide a user-friendly interface for both readers and administrators, featuring a vibrant homepage with breaking news, categorized articles, and extensive user engagement functionalities such as comments and social sharing. The portal is built with a focus on high traffic handling, ensuring reliability and performance for a large audience.

# Project Module Description
- **Core Models**: 
  - **Category**: Hierarchical model for news categories.
  - **Tag**: Model for tagging articles.
  - **Article**: Main content model with fields for title, slug, author, category, tags, image, body, summary, publish date, and status.
  - **Comment**: Model for user comments on articles.
  - **Advertisement**: Model to manage ad placements.

- **Key Functional Requirements**:
  - Homepage with a breaking news ticker and featured articles.
  - Article detail view with comments and related articles.
  - Filtering by category and tags.
  - Search functionality for articles.
  - User registration and authentication.
  - Admin panel for content management.

# Directory Tree
```
news_portal/
│
├── manage.py
├── news/
│   ├── admin.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
├── news_portal/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│
├── templates/
│   ├── base.html
│   ├── news/
│   │   ├── article_detail.html
│   │   ├── category_detail.html
│   │   ├── home.html
│   │   ├── search_results.html
│   ├── registration/
│   │   ├── login.html
│   │   ├── register.html
│
└── requirements.txt
```

# File Description Inventory
- **manage.py**: Command-line utility for administrative tasks.
- **news/**: Application directory containing business logic related to news articles.
- **news_portal/**: Main project directory containing settings and URL configurations.
- **static/**: Directory for static files (CSS, JS, images).
- **templates/**: Directory for HTML templates used in rendering pages.
- **requirements.txt**: Lists project dependencies.

# Technology Stack
- **Framework**: Django 5.2.3
- **Database**: SQLite
- **Frontend**: Bootstrap 5, custom CSS
- **Rich Text Editor**: CKEditor
- **Tag Management**: django-taggit
- **Image Handling**: Pillow

# Usage
1. **Install Dependencies**: 
   ```
   pip install -r requirements.txt
   ```
2. **Run Migrations**: 
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Create Superuser**: 
   ```
   python manage.py createsuperuser
   ```
4. **Run the Server**: 
   ```
   python manage.py runserver
   ```
