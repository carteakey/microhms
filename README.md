# MicroHMS - AI-Enhanced Hotel Management System (2025)

A modern hotel management system powered by artificial intelligence for enhanced guest experience and operational efficiency.

🚀 **NEW in 2025**: AI-powered features including smart pricing, booking assistant, and predictive analytics!

A sample application can be found here https://microhms.onrender.com  (admin / admin@123)

## 🤖 AI Features (2025 Update)

### Intelligent Booking Assistant
- **24/7 AI Chatbot**: Instant guest support for bookings, pricing, and policies
- **Natural Language Processing**: Understands and responds to guest queries in real-time
- **Multi-language Support**: Assist guests in their preferred language

### Smart Pricing Engine
- **Dynamic Pricing**: AI-powered rate optimization based on demand, seasonality, and market conditions
- **Revenue Optimization**: Maximize revenue with intelligent pricing recommendations
- **Competitor Analysis**: Real-time market rate comparisons

### Predictive Analytics
- **Occupancy Forecasting**: Predict future booking patterns and occupancy rates
- **Demand Analysis**: Understand seasonal trends and booking behaviors
- **Revenue Predictions**: Forecast revenue and optimize business strategies

### AI-Driven Insights
- **Analytics Dashboard**: Real-time business intelligence with AI-powered insights
- **Performance Metrics**: Track KPIs with intelligent recommendations
- **Automated Reporting**: Generate detailed reports with AI analysis

## 🏨 Core Features

- Create Bookings, send Booking acknowledgements via email (Mailgun).
- Store guest details & identification and verify through Mobile OTP.
- View Today's & Monthly Bookings.
- Role based access to functionality (Admin/User).
- Create and manage billing entries.
- Generate professional invoices via inbuilt template.
- **NEW**: AI-powered customer service and pricing optimization

### Getting Started

#### Quick Start (2025 Version)
```bash
# Clone the repository
git clone https://github.com/carteakey/microhms.git
cd microhms

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install modern dependencies (2025)
pip install -r requirements_2025.txt
# OR install original dependencies
pip install -r requirements.txt
```

#### Database Setup
```bash
flask db init
flask db migrate
flask db upgrade
```

#### Create Admin User and Sample Data
```bash
python3 -m quickstart
```

#### Run the Application
```bash
flask run
# Application will be available at http://localhost:5000
```

#### Explore AI Features
1. Visit the **AI Analytics Dashboard** for business insights
2. Try the **AI Booking Assistant** for interactive customer support
3. Test **Smart Pricing** recommendations for dynamic rate optimization

### 🐳 Docker Setup (Updated for 2025) 

Use the dockerfile and docker-compose

- Build
```
docker-compose up -d --build         
```

- Create Database tables
```
docker-compose exec web python manage.py create_db
```

- Create an Admin user and sample data.
```
$ docker-compose exec web python manage.py seed_db
Sample data inserted
You can now login with admin/admin@123
You can now create a new user with admin/admin@123

```

- Check the tables for inserted data
```
docker-compose exec db psql --username=microhms --dbname=microhms

microhms=# \c
You are now connected to database "microhms" as user "microhms".

microhms=# select * from public.user;
 id | username |                                                password                                                | active 
----+----------+--------------------------------------------------------------------------------------------------------+--------
  1 | admin    | pbkdf2:sha256:260000$9T1l5qp81l8V6nBU$c7a2597c7a1ae7da919b1b2751e66eb8f65ebc26f199ba89686072e202b5c57d | t
(1 row)
```

## 🚀 What's New in 2025

### AI Integration
- **Booking Assistant**: Intelligent chatbot for instant customer support
- **Smart Analytics**: AI-driven business insights and forecasting  
- **Dynamic Pricing**: Automated rate optimization based on market conditions
- **Predictive Analytics**: Forecast occupancy and revenue trends

### Modern Tech Stack
- Updated to Flask 3.1+ and latest Python packages
- Enhanced security features and performance optimizations
- Modern UI with improved user experience
- Comprehensive test coverage with pytest

### API-First Design
- RESTful APIs for all AI features
- Mobile-ready endpoints for future app integration
- Real-time data synchronization capabilities

### Deployment

This can be deployed to heroku easily using the existing procfile.

```bash
heroku git:remote -a yourappname
git push heroku main
```

Setup environment variables
![Config](/screenshots/config_vars.png)

### Screenshots

|                                                                |                                                                               |                                                                   |
| :------------------------------------------------------------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------: |
|        ![Homepage](/screenshots/homepage.png) Homepage         | ![Guest Verification](/screenshots/guest_verification.png) Guest Verification |      ![Booking](/screenshots/guest_registration.png) Booking      |
| ![Billing Entry](/screenshots/billing_entry.png) Billing Entry |      ![Manage Invoices](/screenshots/print_invoice.png) Manage Invoices       | ![Sample Invoice](/screenshots/sample_invoice.png) Sample Invoice |
| ![Register User](/screenshots/user_register.png) Register User |                  ![Login](/screenshots/user_login.png) Login                  |                                                                   |

### Some things to note

- Mailgun and MSG91 API's are used for Email and OTP respectively. These can be replaced by alternatives in `util.py`.

- Booking page requires an OTP to verify the guest first, for testing purposes 1000 value will bypass this page. **MAKE SURE TO REMOVE THIS LATER.**
