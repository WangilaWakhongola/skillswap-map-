# SkillSwap-Map 🗺️

A real-time,location-based platform that helps people exchange practical skills within their local communities.

## Overview

SkillSwap-Map connects community members who want to share and learn skills. Whether you're looking to teach someone how to cook, fix a bike, or learn a language—this platform makes it easy to find and connect with people nearby.

## Key Features

- 📍 **Real-Time Location Mapping** - Discover skills and people near you on an interactive map
- 👤 **User Profiles** - Showcase your skills and expertise with detailed profiles
- 💬 **Direct Messaging** - Communicate with other users to arrange skill exchanges
- ⭐ **Ratings & Reviews** - Build trust through community reviews
- 📅 **Booking System** - Schedule skill exchange sessions
- 🔔 **Smart Notifications** - Get alerts when someone needs your skill or offers what you want
- 🎯 **Skill Categories** - Browse hundreds of skill categories
- 📊 **Analytics Dashboard** - Track your exchanges and community impact

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Leaflet Maps, Tailwind CSS |
| **Backend** | Django 4.2, Django REST Framework |
| **Database** | PostgreSQL 15 |
| **Real-Time** | WebSockets (Django Channels) |
| **Authentication** | JWT (JSON Web Tokens) |
| **DevOps** | Docker, Docker Compose |
| **API Documentation** | Swagger/OpenAPI |

## Project Structure

```
skillswap-map/
├── backend/               # Django REST API
│   ├── skillswap/        # Main project settings
│   ├── apps/
│   │   ├── users/        # User management & profiles
│   │   ├── skills/       # Skill management
│   │   ├── exchanges/    # Skill exchange logic
│   │   ├── messaging/    # Chat & notifications
│   │   └── locations/    # Geolocation services
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React application
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API calls
│   │   ├── hooks/        # Custom React hooks
│   │   ├── context/      # Context API state
│   │   ├── assets/       # Images, fonts, styles
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── docker/                # Docker configurations
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── env files
├── docs/                  # Documentation
│   ├── API.md            # API Documentation
│   ├── SETUP.md          # Setup & Installation
│   └── DEPLOYMENT.md     # Deployment guide
├── .github/workflows/     # CI/CD pipelines
└── .gitignore
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skillswap-map.git
   cd skillswap-map
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs/

4. **Create superuser** (for admin panel)
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

### Manual Setup (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login & get JWT token
- `POST /api/auth/logout/` - Logout

### Users
- `GET /api/users/` - List users
- `GET /api/users/<id>/` - Get user profile
- `PUT /api/users/<id>/` - Update profile
- `GET /api/users/<id>/skills/` - Get user's skills

### Skills
- `GET /api/skills/` - List all skills
- `POST /api/skills/` - Create new skill offering
- `GET /api/skills/<id>/` - Get skill details
- `PUT /api/skills/<id>/` - Update skill

### Location
- `GET /api/location/nearby/` - Find nearby users with skills
- `POST /api/location/update/` - Update user location

### Exchanges
- `GET /api/exchanges/` - List exchanges
- `POST /api/exchanges/` - Create new exchange request
- `PUT /api/exchanges/<id>/` - Update exchange status
- `GET /api/exchanges/<id>/messages/` - Get exchange messages

### Messaging
- `GET /api/messages/` - List conversations
- `POST /api/messages/` - Send message
- `WebSocket /ws/chat/<exchange_id>/` - Real-time chat

## Development

### Running Tests
```bash
docker-compose exec backend python manage.py test
docker-compose exec frontend npm test
```

### Database Migrations
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Code Quality
```bash
# Lint backend
docker-compose exec backend flake8 .

# Format backend
docker-compose exec backend black .

# Lint frontend
docker-compose exec frontend npm run lint
```

## Environment Variables

Create `.env` file in root directory:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@db:5432/skillswap

# JWT
JWT_SECRET=your-jwt-secret
JWT_EXPIRATION=86400

# AWS/Email (Optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=

# Maps
MAPBOX_TOKEN=your-mapbox-token
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions for:
- AWS EC2
- Heroku
- DigitalOcean
- Google Cloud Platform

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

- **Backend**: PEP 8 (enforced with flake8)
- **Frontend**: ESLint + Prettier
- Use meaningful variable names
- Write docstrings for functions/classes
- Add comments for complex logic

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@skillswap-map.com
- 💬 Discord: [Community Server](https://discord.gg/skillswapmap)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/skillswap-map/issues)

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Video call integration for live skill sessions
- [ ] AI skill recommendations
- [ ] Community badges & achievements
- [ ] Group skill workshops
- [ ] Blockchain-based skill certificates

---

**Built with ❤️ to strengthen local communities through skill sharing**
