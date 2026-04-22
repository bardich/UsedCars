# Full Windsurf Prompt — Django Used Cars Marketplace (Morocco)

## PROJECT OVERVIEW

Build a **premium used cars marketplace website for the Moroccan market** using:

- **Backend:** Django 5+
- **Frontend:** Django Templates
- **CSS:** Tailwind CSS
- **Interactivity:** Alpine.js
- **Database:** PostgreSQL
- **Deployment Ready:** Docker + Nginx + Gunicorn
- **Admin:** Custom Dashboard (NOT default Django admin for business management)
- **Languages:** French / Arabic ready (multilingual architecture)
- **SEO Optimized**
- **Mobile First Responsive Design**

The website will allow admins to manage used cars listings, categories, availability, sold status, and analytics.

Design should be:

- Premium / Modern / Automotive Industry Style
- Fast and Minimal UX
- Moroccan Market Friendly
- Trustworthy and Professional

---

## DEVELOPMENT PHASES

### PHASE 1 — PROJECT INITIALIZATION

Create the Django project architecture professionally.

#### Requirements:

- Setup Django project with modular architecture
- Configure PostgreSQL
- Configure TailwindCSS with Django integration
- Configure Alpine.js globally
- Setup base templates and layout system
- Configure static/media files
- Environment variables with `.env`
- Dockerize project:
  - Dockerfile
  - docker-compose.yml
- Production-ready settings split:
  - base.py
  - dev.py
  - prod.py

#### Structure:

```bash
project/
│
├── apps/
│   ├── core/
│   ├── cars/
│   ├── dashboard/
│   ├── users/
│   └── analytics/
│
├── templates/
├── static/
├── media/
└── config/
```

---

### PHASE 2 — CORE DATABASE MODELS

Create professional models for the used car marketplace.

#### Car Category Model

Fields:

- name
- slug
- icon/image
- description
- is_active

#### Brand Model

Fields:

- name
- slug
- logo

#### Car Model

Fields:

- title
- slug
- category (FK)
- brand (FK)
- model_name
- year
- mileage
- fuel_type
- transmission
- horsepower
- engine_size
- drivetrain
- color
- doors
- seats
- condition
- vin_number (optional)
- registration_city
- description
- price
- negotiable_price (bool)
- featured (bool)
- status:
  - Available
  - Reserved
  - Sold
- published (bool)
- created_at
- updated_at

#### Car Images Model

Fields:

- car (FK)
- image
- alt_text
- is_featured
- order

#### Car Feature Model

For extra options:

- Air Conditioning
- Leather Seats
- Navigation
- Camera
- Bluetooth
- etc.

Many-to-many with Car.

---

### PHASE 3 — FRONTEND PUBLIC WEBSITE

Build the customer-facing marketplace.

#### Homepage Sections

- Hero Banner
- Advanced Car Search
- Featured Cars
- Latest Added Cars
- Browse by Brand
- Browse by Category
- Why Choose Us
- Testimonials
- Contact CTA

#### Cars Listing Page

Filters:

- Brand
- Category
- Price Range
- Year
- Mileage
- Fuel Type
- Transmission
- Status
- Search by keyword

Features:

- Pagination
- Sorting:
  - Newest
  - Price Low/High
  - Mileage
- Grid/List Toggle via Alpine.js

#### Car Detail Page

Include:

- Image Gallery / Slider
- Full Specifications Table
- Features List
- Seller Contact CTA
- WhatsApp Button
- Similar Cars Section
- Availability Badge
- Sold Badge if sold

---

### PHASE 4 — CUSTOM ADMIN DASHBOARD

Build a completely custom business dashboard.

#### Dashboard Overview

Cards for:

- Total Cars
- Available Cars
- Sold Cars
- Reserved Cars
- Featured Cars
- Total Brands
- Total Categories

#### Car Management

Admin can:

- Add New Car
- Edit Car
- Delete Car
- Mark Sold / Available / Reserved
- Toggle Featured
- Upload Multiple Images
- Reorder Images
- Manage Features

#### Category Management

CRUD:

- Add/Edit/Delete Categories

#### Brand Management

CRUD:

- Add/Edit/Delete Brands

---

### PHASE 5 — ANALYTICS & STATISTICS

Create analytics dashboard.

#### Charts / Stats

- Cars Added Per Month
- Sold Cars Per Month
- Most Viewed Cars
- Most Popular Brands
- Inventory By Status
- Revenue Estimate from Sold Cars

Use:

- Chart.js or ApexCharts

---

### PHASE 6 — ADVANCED FEATURES

Implement advanced marketplace functionality.

- Favorites / Wishlist
- Compare Cars
- Inquiry / Lead Form
- WhatsApp Quick Contact

---

### PHASE 7 — SEO OPTIMIZATION

Implement full SEO architecture.

- SEO-friendly slugs
- Dynamic meta titles/descriptions
- OpenGraph tags
- Structured data for cars
- Sitemap.xml
- Robots.txt
- Canonical URLs
- Breadcrumbs

---

### PHASE 8 — MULTILINGUAL READY

Prepare architecture for:

- French
- Arabic
- English future support

Requirements:

- Django i18n enabled
- RTL support for Arabic
- Language switcher component

---

### PHASE 9 — UI/UX DESIGN SYSTEM

#### Style Direction

- Premium Automotive Look
- Dark + White Modern Contrast
- Elegant Typography
- Large Car Imagery
- Smooth Hover Effects
- Subtle Animations
- Card-Based Layout

#### Suggested Color Palette

```txt
Primary: #111827
Secondary: #1F2937
Accent: #DC2626
Gold Highlight: #F59E0B
Background: #F9FAFB
Text: #111827
Muted: #6B7280
```

---

### PHASE 10 — PRODUCTION READINESS

- Secure settings
- Cloud-ready media/static setup
- Logging
- Error pages (404 / 500)
- Performance optimization
- Query optimization
- Caching ready
- Production Docker setup

---

## DEVELOPMENT RULES

### Django Best Practices

- Use Class-Based Views when appropriate
- Keep business logic in services/helpers
- Use Django Forms / ModelForms professionally
- Use custom managers/querysets
- Optimize queries with select_related/prefetch_related

### Frontend Standards

- Tailwind utility-first clean components
- Reusable template partials
- Alpine.js only for lightweight interactivity
- No unnecessary JS frameworks

### Code Quality

- Modular reusable apps
- Clean naming conventions
- Well-commented code
- Production-grade architecture

---

## FINAL OUTPUT EXPECTATION

Build the project phase-by-phase.

After completing each phase:

1. Explain what was built
2. Show folder/file changes
3. Wait for confirmation before moving to next phase

Do NOT generate everything at once.

Proceed sequentially and professionally like a senior software architect.

---

## OPTIONAL BONUS FEATURES

- Import/export inventory CSV
- Dealer CRM mini-module
- API endpoints for mobile app
- Notifications system
- Audit logs for admin actions

---


