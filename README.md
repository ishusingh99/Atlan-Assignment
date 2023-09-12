# Data Collection System

Documentation: `https://docs.google.com/document/d/16_scEz7GVGaKJ7FUcpdqgEyZnpkL0Hg_--oep4su64U/edit?usp=sharing`
Challenge: `https://docs.google.com/document/d/1fsvvkBD8OG_uGuCkF_snG4ZIGXgGOT3tjBagu338408/edit`

## Requirements
- Django==4.0.6
- dynamic-django-forms==0.1.11
- djangorestframework==3.13.1
- gspread==5.10.0
- oauth2client==4.1.3
- oauthlib==3.2.2
- twilio==0.14.3.2


## Steps to run:
1. clone the github repo - `git clone https://github.com/ishusingh99/Demyst-Assignment.git`
2. cd into the Business Load System - `cd '.\Data Collection System\'`
3. run `python manage.py makemigrations`, then `python manage.py migrate` in the terminal.
4. run `python manage.py runserver` in the terminal to run the server.
5. To test APIs, run `http://127.0.0.1:8000/admin/`, so as to populate the Database Models.
6. To test the `send_sms_notification` API, please find the credentials to the twilio account in the documentation or create a trial account on twilio  - `https://www.twilio.com/try-twilio`, and enter the `account_sid`, `auth_token` and `from_phone_number` for the respective account in `send_sms_notification`.

## Entities:
1. Form
2. Question
3. Response

## Database Models:

### 1. Form
The `Form` model represents a form entity within your application, facilitating the creation of structured data collection forms.

Fields:
```
title (CharField): The title of the form, limited to a maximum of 100 characters.
description (TextField): A text description of the form.
```

### 2. Question
The `Question` model represents individual questions associated with a specific form.

Fields:
```
form (ForeignKey to Form): A foreign key relationship connecting questions to their parent form.
text (TextField): The text of the question.
```

### 3. Response
The `Response` model captures user responses submitted for a particular form.

Fields:
```
form (ForeignKey to Form): A foreign key relationship linking responses to their corresponding form.
data (JSONField): A JSON field containing structured response data.
```

## API Details:

### 1. create_form
URL: `http://127.0.0.1:8000/create_form/`

Method: POST

Request Body:
```
{
  "title": "Software Developer",
  "description": "Enter your details to apply for this position.",
  "questions": [
    "Name",
    "Email",
    "Phone Number"
  ]
}
```
Description:
- This API takes `title`, `description` and `questions` (as a list of questions) as request body.
- It inserts `title` and `description` of the form in the `Form` model.
- It inserts every entity of the list `questions` into the `Question` model, creates a form and returns the following response.

Response:
```
{
    "message": "Software Developer Form created"
}
```

### 2. get_response
URL: `http://127.0.0.1:8000/get_response/`

Method: POST

Request Body:
```
{
  "responses": {
    "10": "Shubham Singh",
    "11": "singhshubham5301@gmail.com",
    "12": "+919721242729"
  }
}
```
Description:
- This API takes `responses` (as a dictionary of `question id: response`) as request body.
- It takes `question id: response` from the dictionary `responses` and inserts `question: response` of the form into the `Response` model as a JSONField.
- It also inserts the `question -> column` and the `response -> row` into a Google Sheet and then, returns the following response along with the Google Sheets link.

Response:
```
{
    "message": "Your responses have been recieved. You can access the Google Sheet for your responses in the link below",
    "Link": "https://docs.google.com/spreadsheets/d/1yvsA_bK42OLe3Qm6blOS3kosrt_jRgZnOZ7mv_5HVrU"
}
```
Responses pushed to Google Sheets:

![image](https://github.com/ishusingh99/Atlan-Assignment/assets/55423606/b9300350-e57b-41c0-a359-4d1bcb804f67)

### 3. send_sms_notification
URL: `http://127.0.0.1:8000/send_sms_notification/`

Method: POST

Request Body:
```
{
    "form_id": "4",
    "phone_number": "+919721242729"
}
```
Description:
- This API takes `form_id` and `phone_number` (to send the SMS to) as request body.
- Implements the logic for sending the SMS using the Twilio API.
- It then returns the following response.

Response:
```
{
  "message": "SMS has been sent to +919721242729",
  "data": [
    {
      "id": 9,
      "form_id": 4,
      "data": "{\"Name\": \"Shubham Singh\", \"Email\": \"singhshubham5301@gmail.com\", \"Phone Number\": \"+919721242729\"}"
    }
  ]
}
```
SMS Notification:

![image](https://github.com/ishusingh99/Atlan-Assignment/assets/55423606/8d39bd68-c5fe-47e6-afd0-3f579d9bca7d)

## Additional Details:

#### 1. Authentication Configuration:
The project directory includes a credentials.json file, generated through Google Account, serving as the authentication credential for accessing and manipulating Google Sheets via the Google Sheets API.
#### 2. Utilization of Google Service Accounts:
Google Service Accounts, functioning as automated accounts, have been employed to acquire the necessary credentials. These service accounts enable programmatic access to Google Sheets and associated functionalities.
#### 3. Shared Access via Google Drive:
The sharing mechanism for Google Sheets involves granting access permissions to specific individuals or entities. In this project, the sheets are currently stored within the Google Drive associated with the provided email address (ishusingh99@gmail.com), allowing for shared access with authorized personnel.
#### 4. Database Consistency and Concurrency Control:
Consistency at the database (DB) level is ensured through the implementation of atomic transactions. Additionally, concurrency issues are mitigated by incorporating locking mechanisms within the database operations. These measures collectively maintain the integrity of data and prevent conflicts in concurrent DB interactions.
