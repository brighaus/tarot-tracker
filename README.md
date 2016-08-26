# tarot-tracker
### Python 3 application that lets you enter daily tarot cards then renders reports of trends across time: distribution of suits over time, reverses, etc.

#### Useage
from package root> pip3 install -e .

to make a new daily entry:
>python app/db\_util.py -n

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
  calls init\_data methods to create a shelf database with sample data
- models
  - card: data model for a tarot card
  - daily\_tt: data model for a daily tarot card pull
- read\_db.py
  - CLI access for running lightweight queries against the database
- report.py
  - class for managing the display of the data
- report\_client.py
  - client giving a CLI for generating reports
- test
  - container for test classes
    - pip3 install nose
    - from package root> nosetest -v
