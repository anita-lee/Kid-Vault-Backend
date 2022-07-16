# Welcome to Kid Vault Back-End

## ABOUT

This **Flask API** serves as the back-end for the **Kid Vault** app, which was built as part of the [StepZen](https://stepzen.com/) [GraphQL](https://graphql.org/) Challenge 2022.

The React front-end and **StepZen GraphQL API** code repositories can be viewed here:

- [React Front-end](https://github.com/melawong/mom-api-frontend)
- [StepZen GraphQL API](https://github.com/anita-lee/test_stepzen)

The deployed version of this Flask back-end with a mock Postgres database is viewable here:

- [Heroku Back-end with Postgres data](https://test-mom-api.herokuapp.com/)

`NOTE:` _Heroku often takes some time to wake up! Don't forget to give it a minute._

The deployed version of our app is viewable here:

- [Kid Vault](https://kidvault.surge.sh/)

---

## INSTALLATION

To install this repository on your computer, please follow these instructions:

### Installing Dependencies

```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

### Running this Back-end

1. Create .env file with:

```
DATABASE_URL=postgresql:///mom_api2
SECRET_KEY=[YOUR_SECRET_KEY_HERE]
```

2. Create the database:

```
$ psql
# CREATE DATABASE mom_api2;
```

5. Run `seed.py` file in the project root directory to create the database tables:

```
$ python3 seed.py
```

You only need to do this once, unless you change your model definitions.

4. Fix the database (Data was entered explicitly using .csv files, so we need to set max student_id value):

```
# psql
# \c mom_api2;
# SELECT setval('students_id_seq', (SELECT MAX(id) from "students"));
```

5. Run the app itself:

```
$ flask run -p 5002
```

Visit [http://localhost:5002/](http://localhost:5002/) in your browser to see the results.

---

## WOOHOO!

You Made It! Enjoy and please contact @melawong and @anita-lee with any issues or questions.