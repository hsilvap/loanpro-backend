# Welcome to the challenge backend.
 
## Services
Services are serverless functions that have been deployed to AWS Lambda. The deployment was made by creating a .zip file and manually upload it to each function.
<img width="1357" alt="image" src="https://github.com/user-attachments/assets/7d1f916f-db85-4448-a6ee-a87f553bf25e">

## API
The api is managed by AWS API Gateway, its hosted [here](https://6c64q7kx12.execute-api.us-east-2.amazonaws.com/challenge). Authentication has been enabled to this APIs. The API's will return a 404 if the Authorization token isn't present or is malformed.
<img width="1365" alt="image" src="https://github.com/user-attachments/assets/e7aff19a-d035-45be-9a3f-77833e782489">

## Authentication 
Users are managed in AWS Cognito. After a successful login, the lambda `login` is called to cross validate that the user exists in the database, and sets the proper user_id as a custom claim.
<img width="1360" alt="image" src="https://github.com/user-attachments/assets/d7bbf294-799d-4a8b-b620-cbf3933ed7f0">

## Database
Database is hosted in RDS, the engine is postgress.
<img width="1360" alt="image" src="https://github.com/user-attachments/assets/2fa6522d-d926-49ac-a300-80cdadc961a2">

## Running it locally
To run each service // entity, the following .env variables are needed.
`DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_NAME`. Those will be shared if needed // asked.
