# Student Management System

A modern Student management system built with Django REST Framework and Vue.js, providing a robust solution for Student operations management.

## Project Overview

This system is designed to help Students manage their operations efficiently through a web-based interface. It features a secure user authentication system and a responsive front-end interface.

## Technology Stack

### Backend
- Python 3.12
- Django
- Django REST Framework
- SQLite3 Database

### Frontend
- Vue.js 3
- Vite (Build tool)
- Modern JavaScript (ES6+)
- HTML5/CSS3

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.12 or higher
- Node.js (Latest LTS version recommended)
- npm (comes with Node.js)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd projectBackend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix or MacOS:
```bash
source venv/bin/activate
```

4. Install required Python packages:
```bash
pip install django djangorestframework django-cors-headers
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Start the Django development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd projectFrontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Project Structure

### Backend (`projectBackend/`)
- `manage.py` - Django's command-line utility for administrative tasks
- `projectBackend/` - Main project configuration
- `restAPI/` - Django app containing the REST API endpoints
  - `models.py` - Database models
  - `views.py` - API views and logic
  - `urls.py` - API routing
  - `serializer.py` - JSON serialization for API

### Frontend (`projectFrontend/`)
- `src/` - Source code directory
  - `components/` - Reusable Vue components
  - `pages/` - Vue pages/views
  - `routes/` - Vue router configuration
- `public/` - Static files
- `index.html` - Entry HTML file
- `vite.config.js` - Vite configuration

## Features

- User Authentication and Authorization
- Responsive Design
- RESTful API Integration
- Modern UI/UX Design

## API Documentation

The API endpoints are available at:
- User Authentication: `/api/auth/`
- Data Endpoints: `/api/data/`

For detailed API documentation, run the server and visit `/api/docs/`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
