# AutoMaroc - Used Cars Marketplace

A premium used cars marketplace website for the Moroccan market built with Django, Tailwind CSS, and Alpine.js.

## Features

- **Public Website**: Browse cars, advanced search filters, car details
- **Admin Dashboard**: Custom business management dashboard (not Django admin)
- **Analytics**: Statistics and charts for business insights
- **Multilingual Ready**: French/Arabic/English support architecture
- **SEO Optimized**: Meta tags, OpenGraph, structured data
- **Mobile First**: Responsive design for all devices

## Tech Stack

- **Backend**: Django 5+, PostgreSQL
- **Frontend**: Django Templates, Tailwind CSS, Alpine.js
- **Deployment**: Docker, Nginx, Gunicorn

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Node.js 18+ (for Tailwind CSS)

### 1. Clone and Setup Virtual Environment

```bash
cd UsedCars
./setup_venv.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your settings
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb usedcars

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Install Tailwind CSS

```bash
python manage.py tailwind install
python manage.py tailwind build
```

### 5. Run Development Server

Terminal 1 - Tailwind CSS (watch mode):
```bash
python manage.py tailwind start
```

Terminal 2 - Django server:
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Docker Development

```bash
docker-compose up --build
```

Visit: http://localhost:8000

## Project Structure

```
UsedCars/
├── apps/
│   ├── core/          # Base models, utilities
│   ├── cars/          # Car listings, brands, categories
│   ├── dashboard/     # Custom admin dashboard
│   ├── users/         # User management
│   └── analytics/     # Statistics and reports
├── config/            # Django settings
├── templates/           # HTML templates
├── theme/             # Tailwind CSS configuration
├── static/            # Static files
├── media/             # User uploaded files
├── requirements.txt
└── docker-compose.yml
```

## Development Phases

1. **Phase 1** ✅ - Project Initialization (Complete)
2. **Phase 2** - Core Database Models
3. **Phase 3** - Frontend Public Website
4. **Phase 4** - Custom Admin Dashboard
5. **Phase 5** - Analytics & Statistics
6. **Phase 6** - Advanced Features (Favorites, Compare, etc.)
7. **Phase 7** - SEO Optimization
8. **Phase 8** - Multilingual Support
9. **Phase 9** - UI/UX Design System
10. **Phase 10** - Production Readiness

## License

MIT License
