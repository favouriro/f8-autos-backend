# F8 Autos - Backend API

A Django REST API backend for the F8 Autos mechanic and body shop platform. Built with Django, Django REST Framework, and PostgreSQL.

## Live Demo

Backend API: https://f8-autos-backend.onrender.com/api/
Frontend Application: https://f8-autos-frontend.onrender.com

## Project Overview

F8 Autos is a full-stack web application for a mechanic and body shop. The platform allows customers to browse cars for sale, view available services, and submit booking requests. Admins can manage inventory and services through the Django admin panel.

## Features

### Authentication
- User registration with password validation
- JWT token-based authentication (login/logout)
- Protected routes requiring authentication
- User profile endpoint

### Cars
- Browse all cars for sale
- Car details including make, model, year, mileage, price and condition
- Cloudinary image uploads for car photos
- Admin can add, edit and delete cars

### Services & Bookings
- Browse available services and pricing
- Authenticated users can submit booking requests
- Booking confirmation emails sent via SendGrid
- Users can view their own booking history
- Admin can manage all bookings

## Tech Stack

- **Django 4.2** - Python web framework
- **Django REST Framework** - API toolkit
- **PostgreSQL** - Production database
- **Simple JWT** - JWT authentication
- **Cloudinary** - Image storage
- **SendGrid** - Email notifications
- **Gunicorn** - Production web server
- **WhiteNoise** - Static file serving
- **Render** - Cloud deployment

## Project Structure
```
f8-autos-backend/
├── authentication/        # User registration and profile
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── cars/                  # Cars for sale
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── services/              # Services and bookings
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── email.py
│   └── tests.py
├── backend/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

The API will be available at http://127.0.0.1:8000/api/

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /api/auth/register/ | Register a new user | No |
| POST | /api/token/ | Login and get JWT tokens | No |
| POST | /api/token/refresh/ | Refresh access token | No |
| GET | /api/auth/profile/ | Get current user profile | Yes |

### Cars
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/cars/ | List all cars | No |
| GET | /api/cars/{id}/ | Get a specific car | No |
| POST | /api/cars/ | Add a new car | Admin only |
| PUT | /api/cars/{id}/ | Update a car | Admin only |
| DELETE | /api/cars/{id}/ | Delete a car | Admin only |

### Services
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/services/ | List all services | No |
| GET | /api/services/{id}/ | Get a specific service | No |
| POST | /api/services/ | Add a new service | Admin only |

### Bookings
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/bookings/ | List user's bookings | Yes |
| POST | /api/bookings/ | Create a booking | Yes |

## Running Tests
```bash
python manage.py test
```
Expected output: 14 tests passing

## Architecture Decisions

**JWT Authentication** was chosen over session-based auth because it is stateless and works well with a separate React frontend — the token is stored in the browser and sent with every request.

**Cloudinary** is used for image storage rather than storing images on the server, because server storage would be lost on Render's free tier and doesn't scale well.

**SendGrid** handles transactional emails because it provides reliable email delivery and a generous free tier suitable for this application.

**Separation of apps** — the project is split into three Django apps (authentication, cars, services) following Django's recommended approach of keeping each app focused on a single area of functionality.

## Deployment

The application is deployed on Render. See the environment variables section for all required production variables. The build command runs migrations and collects static files automatically on each deploy.

## Environment Variables

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | Set to False in production |
| DATABASE_URL | PostgreSQL connection string (set automatically by Render) |
| RENDER_EXTERNAL_HOSTNAME | Render service hostname |
| FRONTEND_URL | Deployed frontend URL for CORS |
| SENDGRID_API_KEY | SendGrid API key for emails |
| DEFAULT_FROM_EMAIL | Verified sender email address |
| CLOUDINARY_CLOUD_NAME | Cloudinary cloud name |
| CLOUDINARY_API_KEY | Cloudinary API key |
| CLOUDINARY_API_SECRET | Cloudinary API secret |

## AI Use Acknowledgement

Generative AI was used throughout the development 
of this project in the following ways:

- **Planning** — helping scope the application features
- **Guidance** — Explanations of Django and React concepts 
  as they were implemented, including models, serializers, ViewSets, 
  React hooks, and JWT authentication flow
- **Debugging** — identifying and explaining errors such as CORS 
  misconfigurations, dependency conflicts in requirements.txt etc
- Refinement of README
