# MicroHMS

A sample application can be found here https://microhms.onrender.com  (admin / admin@123)

### Features

- Create Bookings, send Booking acknowledgements via email (Mailgun).
- Store guest details & identification and verify through Mobile OTP.
- View Today's & Monthly Bookings.
- Role based access to functionality (Admin/User).
- Create and manage billing entries.
- Generate professional invoices via inbuilt template.

### Getting Started

- Setup database (heroku-postgresql hobby-dev is a great free option).
- Add database URL to .env file (example provided).
- Setup API keys in .env file as per need.
- Setup a local environment.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

- Upgrade database to our model.

```bash
flask db init
flask db migrate
flask db upgrade
```

- Create an Admin user and sample data.

```bash
python3 -m quickstart
```

- Run your application

```
flask run
```

# OR 

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
