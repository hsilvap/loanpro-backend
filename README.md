# Welcome to the challenge backend.
 
## Services
Services are serverless functions that have been deployed to AWS Lambda. The deployment was made by creating a .zip file and manually upload it to each function.
<img width="1357" alt="image" src="https://github.com/user-attachments/assets/8051f178-0162-47b0-8705-a5aa10a03308">

## API
The api is managed by AWS API Gateway, its hosted [here](https://6c64q7kx12.execute-api.us-east-2.amazonaws.com/challenge). Authentication has been enabled to this APIs. The API's will return a 404 if the Authorization token isn't present or is malformed.
The full API details are [here](https://drive.google.com/file/d/1G8PQDBs6LkWEzRupNBVDZ2RwrJM5JaI6/view?usp=sharing). It needs to be used with postman 
<img width="1365" alt="image" src="https://github.com/user-attachments/assets/e7aff19a-d035-45be-9a3f-77833e782489">

## Authentication 
Users are managed in AWS Cognito. After a successful login, the lambda `login` is called to cross validate that the user exists in the database, and sets the proper user_id as a custom claim.
<img width="1360" alt="image" src="https://github.com/user-attachments/assets/d7bbf294-799d-4a8b-b620-cbf3933ed7f0">

## Database
Database is hosted in RDS, the engine is postgress.
<img width="1360" alt="image" src="https://github.com/user-attachments/assets/2fa6522d-d926-49ac-a300-80cdadc961a2">

## Running it locally
To run each service // entity, the following .env variables are needed. Python 3.12 is recommended, and use of venv per service directory.
`DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_NAME`. Those will be shared if needed // asked.
Venv is recommended per directory, do
1. `pip install venv`
2. `python3 -m venv venv` 
3. `source venv/bin/activate`
