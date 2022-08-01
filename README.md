# MicroHMS

A sample application can be found here https://microhms.herokuapp.com (admin / admin@123)

### Features
- Create Bookings, send Booking acknowledgements via email (Mailgun)
- Store guest details & identification and verify through Mobile OTP
- Role based access to functionality (Admin/User)
- Create and manage billing entries
- Generate professional invoices via inbuilt template

### Getting Started
- Setup database (heroku-postgresql hobby-dev is a great free option)
- Add database URL to .env file (example provided)
- Setup API keys in .env file as per need.
- Setup a local environment
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
- Upgrade database to our model
```bash
flask db init
flask db migrate
flask db upgrade
```

- Create an Admin user and sample data
```bash
python3 -m quickstart
```
- Run your application
```
flask run
```

### Deployment
This can be deployed to heroku easily using the existing procfile
```bash
heroku git:remote -a yourappname
git push heroku main
```
Setup environment variables
![Config](/screenshots/config_vars.png) 

### Screenshots
| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|![Homepage](/screenshots/homepage.png) Homepage |![Guest Verification](/screenshots/guest_verification.png) Guest Verification | ![Booking](/screenshots/guest_registration.png) Booking|
|![Billing Entry](/screenshots/billing_entry.png) Billing Entry |![Manage Invoices](/screenshots/print_invoice.png) Manage Invoices | ![Sample Invoice](/screenshots/sample_invoice.png) Sample Invoice|
|![Register User](/screenshots/user_register.png) Register User |![Login](/screenshots/user_login.png) Login | |

### Some things to note
- Mailgun and MSG91 API's are used for Email and OTP respectively. These can be replaced by alternatives in `util.py`.

- Booking page requires an OTP to verify the guest first, for testing purposes 1000 value will bypass this page. **MAKE SURE TO REMOVE THIS LATER.**


To be added in future releases
- Page to edit invoices
- Page to manage bookings
