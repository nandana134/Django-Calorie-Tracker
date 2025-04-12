# Django Calorie Tracker

A web application built with Django that allows users to track their daily calorie intake, set goals, and view nutritional summaries. The project focuses on simplicity and useful features like PDF report generation and daily email reminders for inactive users.

---

## 🌟 Features

- ✅ **User Registration and Login**
- ✅ **Add/Search Food Items**
  - Smart dropdown that filters food items based on typed characters.
- ✅ **Interactive Dashboard**
  - Table listing consumed food items.
  - Ability to delete or update entries.
- ✅ **Nutrient Pie Chart**
  - Visual representation of daily nutrient breakdown (carbs, protein, fat).
- ✅ **Profile Section**
  - Date and time-wise history of consumed food.
- ✅ **Daily Calorie Goal Setting**
  - Allows user to set a calorie limit.
  - Displays real-time feedback if the user exceeds or is under the goal.
- ✅ **PDF Report Generation**
  - Includes username, email, food consumed, calorie goal, total calories, and summary.
  - Clean format using **xhtml2pdf**.
- ✅ **Daily Reminder Email**
  - Automatically sends a reminder email at 7 PM to users who didn’t log any food for the day.

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (default Django DB)
- **Charting**: Chart.js
- **PDF Generation**: xhtml2pdf
- **Email**: Django Email Backend

---

## 🚀 How to Run This Project Locally

### 1. Clone the Repository

git clone https://github.com/nandana134/django-calorie-tracker.git
cd django-calorie-tracker/mysite

### 2. Create Virtual Environment

python -m venv venv

venv\Scripts\activate     # On Windows


source venv/bin/activate  # On Mac/Linux

### 3. Install Requirements

pip install -r requirements.txt

### 4. Run Migrations

python manage.py makemigrations

python manage.py migrate

### 5. Create Superuser(Optional for Admin Panel)

python manage.py createsuperuser

### 🧠 How to Add Food Data
Note: The food data in food1.csv is for demonstration purposes only and may not be accurate or verified.
Food items (used in the dropdown list) are stored in the database. You can import them using the following command:
```
python manage.py import_food
```
This reads from a CSV file (food1.csv) and populates the Food model.

***🔐 Note: A temporary import_food_data view was added for deployment use only. It has been removed for security. Please use the custom command instead.***

### 6. Start the Server
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser.

### Email Reminder Setup (for Daily Reminders)

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'  # (16-char Google app password, not your original password)
```

You can schedule the email reminder script using a **cron job** or **Windows Task Scheduler** to run every day at **7 PM**.

### 🌍 Deployment Notes
This project was deployed on Render using GitHub integration.

### 💡 Contributing
Feel free to fork the project and open pull requests! Contributions are welcome to add features like:
-🗓️ Weekly/Monthly summaries
-📱 REST API support
-📊 Export reports as Excel


**License**

This project is open-source and available under the MIT License.








