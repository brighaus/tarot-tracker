# tarot-tracker
### Python 3 application that lets you enter daily tarot cards then renders reports of trends across time: distribution of suits over time, reverses, etc.

#### Useage
- from package root> `pip3 install -e .`
- create sample database: see *make\_db* below
- to make a new daily entry:
  - $> `python3 app/db_util.py -n`

**app:**
- data\_manager.py
  - manages the data at the cache level, only calling file i/o when cache goes stale
  - has test coverage, see: test
- data\_mule.py
  - handles file i/o
- db\_config.py
  - databse constants
- db\_util.py
  - Accesses the datamanager to make CRUD manipulations on the db. 
- init\_data.py
  - parses raw data from csv files with sample data
- input\_client.py
  - TKinter popup window input client
- make\_db.py
  - calls init\_data methods to create a shelf database with sample data
  - to build a db from sample data:
    1. (from tarot-tracker root)$> `rm data tarot_dailies*`
      - this removes both test and prod dbs
    1. (from python REPL or script) `import app.make_db as mdb`
    1. `mdb.dump_db()` or `mdb.dump_test_db()`
- models
  - card: data model for a tarot card
  - daily\_tt: data model for a daily tarot card pull
- read\_db.py
  - CLI access for running lightweight queries against the database
- report.py
  - class for managing the display of the data
- report\_client.py
  - client giving a CLI for generating reports
  - get help:
    - $> `python3 app/report_client.py -h`
  - generating a test report after running *make\_db* (above):
    - $> `python3 app/report_client.py -r  -t suit_rank_date -dr '06/01/2014|07/01/2014' -f html`
      
- test
  - container for test classes
    - pip3 install nose
    - from package root> nosetests -v
