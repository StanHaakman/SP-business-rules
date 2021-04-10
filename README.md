# SP-business-rules
We gaan aan het werk met het opzetten van een rule-based systeem ten behoeve van de recommendation engine.

## Pre requirements
For this project you need to install a number of python libraries. To do that run this command:
This will install all the packages.

```pip install -r requirements.txt```
If this doesn't work you can find a list of the required libraries in the requirements.txt file

You also have to have MongoDB and Postgresql installed

## Setup
First add a file to the project folder called, database.ini, in this file we will put the info for the database connection.

```[postgresql]
host = localhost
password = postgres
user = postgres
database = huwebshop 
```

After this you can run this command to create and fill the database with the correct data with this command:

``` python3 database_interactions/main_data_to_postgres.py ```

Now follow the setup and launch tutorial in the README_WEBSHOP.md
