This project has three repositories.

1. Flask API Back-End: mom_api2

2. StepZen: test_stepzen

3. React Front-End: mom-api-frontend





Use Insomnia to add Mom & School profile:
```
{ "username":"Mom",
"password":"password",
"first_name":"Laura",
"last_name":"Andooli",
"email":"l@andooli.com",
"phone":"3425435"}

{ "username":"school",
"password":"school",
"first_name":"school",
"last_name":"school",
"email":"school@school.com",
"phone":"3425435"}
```

Use Insomnia to add Guardian/Children Relationships for Andooli Family:
```
{ "guardian_username":"Mom",
"child_id":"4" }

{ "guardian_username":"Mom",
"child_id":"6" }

{ "guardian_username":"Mom",
"child_id":"7" }
```

3. React Front-End => mom-api-frontend

### Installing Dependencies

```
npm install
```

### Running the Front End

Create .env file with:
```
REACT_APP_API_KEY=*******
REACT_APP_BASE_URL=*******
```
******** = Provide your own.

Then run React:

```
$ npm start
```
