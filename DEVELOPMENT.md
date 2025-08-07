# Development Configuration for MicroHMS (2025)

## Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- Virtual environment (recommended)

## Quick Setup (2025 Version)

### 1. Clone and Setup
```bash
git clone https://github.com/carteakey/microhms.git
cd microhms
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# For development with latest packages (2025)
pip install -r requirements_2025.txt

# Or for production compatibility
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
cp .env.dev .env
# Edit .env file with your configuration
```

### 4. Database Setup
```bash
flask db init
flask db migrate
flask db upgrade
```

### 5. Create Admin User and Sample Data
```bash
python -m quickstart
```

### 6. Run Application
```bash
flask run
# Or for development
python -m flask --app project run --debug
```

## New AI Features (2025)

### AI-Powered Booking Assistant
- Instant customer support chatbot
- Natural language booking assistance
- 24/7 availability for guest queries

### Smart Pricing Engine
- Dynamic room rate optimization
- Demand-based pricing recommendations
- Seasonal and occupancy adjustments

### Predictive Analytics
- Occupancy forecasting
- Revenue predictions
- Demand pattern analysis

### Analytics Dashboard
- Real-time business insights
- AI-driven recommendations
- Visual data representations

## Development Tools

### Code Formatting
```bash
black project/ tests/
```

### Linting
```bash
flake8 project/ tests/
```

### Testing
```bash
pytest
pytest --cov=project
```

## Docker Development (Updated)
```bash
docker-compose up -d --build
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db
```

## API Endpoints (New in 2025)

### AI Features
- `GET /ai/chatbot` - AI chatbot interface
- `POST /ai/chat` - Chat with AI assistant
- `POST /ai/pricing/recommend` - Get pricing recommendations
- `POST /ai/occupancy/predict` - Predict occupancy
- `GET /ai/analytics/dashboard` - Analytics dashboard
- `GET /ai/analytics/data` - Analytics data API

## Technology Stack (2025)
- **Backend**: Flask 3.1.0, SQLAlchemy 2.0
- **Database**: PostgreSQL / SQLite
- **AI/ML**: scikit-learn, pandas, numpy
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Testing**: pytest, pytest-flask
- **Development**: black, flake8, pre-commit

## Configuration

### Environment Variables
```
FLASK_APP=project
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost/microhms
SECRET_KEY=your-secret-key
MSG91_AUTHKEY=your-msg91-key
MAILGUN_API_KEY=your-mailgun-key
MAILGUN_DOMAIN=your-domain
```

### AI Feature Configuration
AI features work out of the box with built-in algorithms. For advanced features:
- Configure OpenAI API key for enhanced NLP
- Set up external analytics services
- Configure ML model endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## License
MIT License - see LICENSE file for details