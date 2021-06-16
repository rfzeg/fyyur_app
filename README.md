Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.


## Tech Stack (Dependencies)

 Besides **Python 3**, here are the other required components:

### 1. Backend Dependencies

 * **Conda** to manage dependencies
 * **SQLAlchemy ORM** as the ORM library of choice
 * **PostgreSQL** as the database of choice
 * **Flask** as the server framework
 * **Flask-Migrate** for creating and running schema migrations

You can create the environment from the environment.yml file like so:  

```
conda env create -f environment.yml
```

### 2. Frontend Dependencies

* **Google Chrome** to show **HTML**, **CSS** and **Javascript**.


## Usage:

1. **Start a Postgres server on your local machine:**  
From within your virtual environment, `cd` to the parent directory of your database cluster folder (in this example 'my_db_cluster'), then run:  
`pg_ctl -D my_db_cluster start`  

2. **Run the development server:**
```
python3 app.py
```

3. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 


## Starter code

This Web App is based on the following project starter files:  

```
https://github.com/udacity/FSND/tree/master/projects/01_fyyur/starter_code
```