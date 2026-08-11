# ☕ Cafe Finder

A full-featured web application to discover, manage, and explore cafes with good coffee, WiFi, and power outlets. Built with Flask, SQLite, and Bootstrap.

## 🌟 Features

### Public Features
- **Browse Cafes** - View all cafes in a clean, responsive grid layout
- **Search Cafes** - Find cafes near any location
- **View Details** - See amenities (WiFi, sockets, toilets), coffee prices, and seating capacity
- **Interactive UI** - Professional Bootstrap 4 design with Font Awesome icons

### Admin Features (Login Required)
- **Add Cafes** - Manually add new cafes with all details
- **Edit Cafes** - Update cafe information anytime
- **Delete Cafes** - Remove cafes that are closed or incorrect
- **Auto-Scrape** - Automatically import cafes from OpenStreetMap using Overpass API
- **Admin Dashboard** - Badge indicator when logged in

### Technical Features
- **REST API** - Full CRUD API endpoints for programmatic access
- **Database** - SQLite with SQLAlchemy ORM
- **Authentication** - Secure admin login with Flask-Login
- **Web Scraping** - OpenStreetMap integration for automatic cafe discovery
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Flash Messages** - User feedback with auto-dismiss notifications

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask** | Python web framework |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Lightweight database |
| **Flask-Login** | User authentication |
| **Bootstrap 4** | Frontend framework |
| **Font Awesome** | Icons |
| **OpenStreetMap API** | Cafe data source |
| **Overpass API** | Cafe querying |

## 📁 Project Structure
