# Mom_API - Reducing paperwork for busy moms.

## Description

Mom_API leverages the power of [GraphQL](https://graphql.org/) with [StepZen](https://stepzen.com/) to generate custom queries to complete school forms. This MVP focuses on the **Blue Card (emergency contact information)** which needs to be duplicated each time a child attends a camp, after-school program, or school. Organizations each have their own record-keeping system.  Our solution empowers the parent -
A: Choose QR code with their child's information from their main school org to share with local organizations.
B: Host their child's information on blockchain so they are in full control.

Since these organizations don't share data, we give the parent the power to enter their children's information once, which can then be queried via a Metamask-type front-end browser
extension to autopopulate school forms via [ML text recognition](https://developers.google.com/ml-kit/vision/text-recognition/).

We hope in the future that schools can access these parent's database via an API authorization token, thereby
reducing duplicate paperwork for busy parents.

## DEMO

## Getting Started

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

### Running the app

Create .env file with:
```
DATABASE_URL=postgresql:///mom_api
```

Create the database:
```
$ psql
# CREATE DATABASE mom_api;
```
Fix the database: (Data was entered explicitly using .csv files, need to set max student_id value)
```
# SELECT setval('students_id_seq', (SELECT MAX(id) from "students"));
```

To run the app, first run the `seed.py` file directly to create the database tables:

```
$ python3 seed.py
```

You only need to do this once, unless you change your model definitions.

NOT SET UP YET>>>> Then run the app itself:

```
$ flask run -p 5001
```

Visit [http://localhost:5001/](http://localhost:5001/) in your browser to see the results.
`
## Future
1. Testing
2. Expanding the type of information stored in the mom_api database
3. Integrate ML text recognition for easy auto-population
4. Create QR code abilities so schools can easily download the information from the parent.  Similar to scanning in a child.
5. Create HIPAA compliant way for medical organizations to upload child's vaccination records/medical history.

## Acknowledgments

Inspiration, code snippets, etc.

