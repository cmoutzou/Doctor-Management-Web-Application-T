{
  "name": "Pulmonologist",
  "description": "Pulmonologist-CC",
  "image": "heroku/python",
  "repository": "https://github.com/heroku/pulmonologist",
  "keywords": ["python", "django" ],
  "addons": [ "heroku-postgresql" ],
  "env": {
    "SECRET_KEY": {
      "description": "Pulmonologist.",
      "generator": "secret"
    }
  },
  "environments": {
    "test": {
      "scripts": {
        "test-setup": "python manage.py collectstatic --noinput",
        "test": "python manage.py test"
      }
    }
  }
}
