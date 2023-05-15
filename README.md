# Jobs test task

# Run the application

Mandatory steps:

```bash
# The .env.default is prepared to be used with Docker by default
cp .env.default .env
```

Run using docker-compose

```bash
docker-compose up --build -d
```

Run using local tools:

- Install Python3.11
- Install PostgreSQL
- Create the database table

```bash
# Install the dependencies managing tool
pip install pipenv

# Activate the environment
pipenv shell

# Install dependencies
pipenv sync

# Migrate to the latest database version
python manage.py migrate

# Run the server
python manage.py runserver
```

# Disclaimer

- Since the authentication method is not provided in the specification the JWT is used
  > Note: There is no endpoint for user creation. Use the Django CLI for doing this.
  ```bash
  (jobs) ➜ jobs python manage.py createsuperuser
  Email address: admin@admin.com
  Password:
  Password (again):
  Superuser created successfully.
  (jobs) ➜ jobs
  ```
  > Or create in docker container using docker-compose
  ```bash
  docker-compose exec app python manage.py createsuperuser
  ```

### About exceptions

⚠️ Since it is not specified which sort of exceptions should be returned - 500 are used with default `APIExceptin`

# The example of database data:

⚠️ Since it is not specified what should be done with the data once the related model is removed the RESTRICTED method is chosed

Only the job with job_header use the CASCADE removing according to the requirements

#### users

| id  | ussername |
| --- | --------- |
| 1   | admin     |

#### jobs headers

| id  | rich_title_text         | rich_subtitle_text               |
| --- | ----------------------- | -------------------------------- |
| 1   | `<h1>Backend dev</h1>`  | `<h2>Backend dev subtitle</h2>`  |
| 2   | `<h1>Frontend dev</h1>` | `<h2>Frontend dev subtitle</h2>` |

#### jobs

`job_header_id` relation is One2Many

| id  | name         | type      | job_header_id |
| --- | ------------ | --------- | ------------- |
| 1   | Backend dev  | Full time | 1             |
| 2   | Frontend dev | Part time | 2             |

#### applications

The `job_id` relation One2One, then it is restricted to have duplication of job_id in the table
`user_id` relation is One2Many

| id  | job_id | user_id |
| --- | ------ | ------- |
| 1   | 1      | 1       |
| 2   | 2      | 1       |

# About API router

### Auth

- `HTTP POST /auth/jwt/create/` - Create the access and refresh tokens
- `HTTP POST /auth/jwt/refresh/` - Refresh the access token

### Jobs

- `HTTP POST /jobs/` - Create job and related job headers
- `HTTP PUT /jobs/<id>/` - Update job and related job headers (Does not work for partial updating since it is not defined in requirements)
- `HTTP DELETE /jobs/<id>/` - Delete job and related job headers

### Applications

- `HTTP GET /applications/` - Get all user's applications
