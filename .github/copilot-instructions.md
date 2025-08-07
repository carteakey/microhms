# MicroHMS - Hotel Management System

MicroHMS is a Flask-based Hotel Management System with PostgreSQL database that supports creating bookings, guest management, billing, and invoice generation. The application supports both local development and Docker deployment.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### System Requirements and Setup
- Install system dependencies first:
  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-pip libpq-dev build-essential libcairo2-dev libpango1.0-dev
  ```

### Local Development Setup
- Create and activate Python virtual environment:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```
- Install Python dependencies -- CRITICAL: may fail due to PyPI connectivity issues. Use retries and increased timeouts:
  ```bash
  pip install --timeout 300 --retries 5 -r requirements.txt
  ```
  - If this fails with timeout errors, retry the command multiple times
  - In environments with network restrictions, this may require multiple attempts over 10-15 minutes
  - Consider installing key packages individually: `pip install flask flask-sqlalchemy flask-migrate psycopg2-binary`

### Database Setup (Local)
- You need a PostgreSQL database. Set up the DATABASE_URL in `.env` file based on `.env.dev` template:
  ```bash
  cp .env.dev .env
  # Edit .env with your database connection details
  ```
- Initialize database migrations:
  ```bash
  source env/bin/activate
  flask db init    # NEVER CANCEL: may take 30 seconds
  flask db migrate # NEVER CANCEL: may take 1-2 minutes  
  flask db upgrade # NEVER CANCEL: may take 1-2 minutes
  ```
- Create admin user and sample data:
  ```bash
  python3 -m quickstart  # Takes 10-30 seconds
  ```

### Docker Development Setup (Recommended)
- Build and start containers -- NEVER CANCEL: Build takes 10-15 minutes on first run due to pip install:
  ```bash
  docker compose up -d --build  # Set timeout to 20+ minutes
  ```
- Initialize database in Docker:
  ```bash
  docker compose exec web python manage.py create_db  # Takes 10-30 seconds
  docker compose exec web python manage.py seed_db    # Takes 10-30 seconds
  ```
- Access database directly if needed:
  ```bash
  docker compose exec db psql --username=microhms --dbname=microhms
  ```

### Running the Application
- Local development:
  ```bash
  source env/bin/activate
  flask run  # Starts on http://localhost:5000
  ```
- Docker:
  ```bash
  docker compose up  # Access on http://localhost:8000
  ```

### Code Quality and Linting
- Format code with black (if successfully installed):
  ```bash
  source env/bin/activate
  black project/ *.py  # Format all Python files
  ```
- Check code style with pycodestyle (if successfully installed):
  ```bash
  source env/bin/activate
  pycodestyle project/ *.py
  ```
- NOTE: Linting tools may fail to install due to network connectivity issues

## Validation

### Manual Testing Required
- Always manually test the application after making changes
- Login credentials: admin / admin@123
- Test key workflows:
  1. Login with admin credentials
  2. Create a new booking (use OTP bypass value: 1000 for testing)
  3. View booking list and details
  4. Create billing entries
  5. Generate and view invoices
- The application includes OTP verification - use 1000 as bypass value during development

### Application Structure
- Main application entry: `manage.py`
- Flask app factory: `project/__init__.py`
- Models: `project/models.py`
- Routes organized in blueprints:
  - Main routes: `project/main.py`
  - Login: `project/login/routes.py`
  - Registration: `project/registration/routes.py`
  - Invoice: `project/invoice/routes.py`
- Templates: `project/templates/`
- Static files: `project/static/`

## Known Issues and Workarounds

### Network Connectivity Issues
- `pip install -r requirements.txt` frequently fails with timeout errors
- Docker builds may fail for the same reason
- Workarounds:
  - Retry commands multiple times with increased timeouts
  - Install packages individually: `pip install flask flask-sqlalchemy flask-migrate`
  - Use `--timeout 300 --retries 5` flags with pip
  - In some environments, allow 15-20 minutes for dependency installation

### Database Notes
- Application requires PostgreSQL database
- Database connection configured via DATABASE_URL environment variable
- Sample data includes test user (admin/admin@123) and basic configuration
- OTP verification can be bypassed with value "1000" for development

### Testing Notes
- No automated test suite is currently present in the repository
- All validation must be done manually through the web interface
- Key test scenarios:
  - User authentication
  - Booking creation and management
  - Billing and invoice generation
  - Guest verification workflow

## Common Commands Reference

### Repository Structure
```
.
├── README.md              # Setup documentation
├── requirements.txt       # Python dependencies
├── manage.py             # Main application entry point
├── quickstart.py         # Sample data creation
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Multi-container setup
├── build.sh             # Basic setup script
└── project/             # Main application directory
    ├── __init__.py      # Flask app factory
    ├── models.py        # Database models
    ├── main.py          # Main routes
    ├── util.py          # Utilities (email, SMS)
    ├── templates/       # Jinja2 templates
    ├── static/          # CSS, JS, images
    ├── login/           # Authentication module
    ├── registration/    # Booking module
    └── invoice/         # Billing module
```

### Essential Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Flask session security
- `MAILGUN_API_KEY`: Email service (optional)
- `MSG91_AUTHKEY`: SMS/OTP service (optional)

### Database Quick Commands
```bash
# Local database operations
source env/bin/activate
flask db migrate -m "description"
flask db upgrade

# Docker database operations
docker compose exec web python manage.py create_db
docker compose exec web python manage.py seed_db
```

## Development Tips
- Always activate virtual environment before running local commands
- Use Docker for consistent development environment
- Test email/SMS features require API keys in environment variables
- Application uses Bootstrap 5 with Zephyr theme
- PDF invoice generation uses WeasyPrint library (requires system dependencies)
- Guest verification feature uses OTP - bypass with "1000" for testing