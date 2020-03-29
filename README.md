# social-network-rest-api

This is test task for job interview. 
Task includes creating a sample social network API using Django and DRF. Any batteries are alloved and optional.

Basic part of a project are:
* User creation with email as a login.
* JWT token auth.
* Post that can be created by authorized user.
* Post like and dislike.
* Unittests for created views.

Optional:
* Email verification with hanter.io on sign up.
* Additional user data with clearbit.com

To setup and run project you have to have docker installed on your OS.
Execute folloving commands inside project directory:

>$ docker build .

>$ docker-compose run webapp python /src/manage.py migrate

>$ docker-compose run webapp python /src/manage.py test

>$ docker-compose up --build

To create new user run request like that: 
Use your organisation domain email since, emailhunter will not validate simple mailservices like @gmail.com
Or change settings.USE_EMAIL_VERIFIER to False to disable email varification.

>$ curl --location --request POST 'http://127.0.0.1:8000/api/users/register/' \
--form 'email=workemail@oraganisation.domain' \
--form 'password=superduper1password' \
--form 'password2=superduper1password'

To obtain JWT token run
>$ curl --location --request POST 'http://127.0.0.1:8000/api/token/' \
--form 'email=workemail@oraganisation.domain' \
--form 'password=superduper1password'

Use obtained accsess token as an 'Authorization: Bearer token' header to perform authorized reqeusts.
Authorized user can create or delete Posts and Like/Unlike them.

For API documentation visit:
> http://localhost:8000/redoc/
