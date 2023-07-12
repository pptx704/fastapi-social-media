# Fastapi Demo Social Media
This repo contains a very small social media made with Fastapi.
User can:
- Create an account
- Post something
- Edit/Delete a post
- View all posts
- Like/Dislike other people's post

# How to run
1. Clone this repo
2. Modify the `docker-compose.yml` file to change environment variables (specially `HUNTER_API_KEY` for [hunter.io](https://hunter.io) should be added). 
3. Setting a docker volume for the database is recommended.
4. Run `docker-compose up --build` with optional `-d` flag to run in background
5. Go to `localhost:8000/docs` to see the Swagger documentation

# Workflow
1. User registers an account on `/register` endpoint
2. They login on `/login` endpoint to get a JWT token. This token has to be passed as `Authorization: Bearer <token>` header for all other endpoints. Token expires in 4 hours.
3. If user is not verified, `/send-verification` is used to send a verification link to their email (instead of sending the email, for now it is returned in the response).
4. User verifies their account by going to `/verify/<code>` endpoint.
5. If everything goes well `/current-user` will return the user's information.
6. The `/post` endpoints are self-explanatory.