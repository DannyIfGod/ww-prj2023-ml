
# Backend Service

This is the backend web service of the app. It is a Python Flask app.

# Run local development

## Frontend - react.b

    `cd react.b`
    `npm run start`

# BACKEND
        
        `flask --app backend run`, or 
        `python -m flask --app backend run`, or
        `./start-backend.bat`

        or
        `gunicorn 'src:create_app()'`  (PROD mode)