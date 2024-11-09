# Requirements
python 3 installed.  I think that's all?
# Setup
## Windows
1. open powershell
2. cd to this directory
3. pip install -r requirements.txt
4. python3 run.py migrate
## Linux
1. open bash
2. cd to this directory
3. pip install -r requirements.txt
4. python3 run.py migrate

# Running the solver
1. set up your database.  At the moment there is no application for this, connect to the var/data.db file with your preferred sqlite client (I used heidisql)
    * optionally import a quick demo using the var/demo.sql
2. run python3 run.py generateRota