# Requirements
python 3 installed.  I think that's all?
# Setup
## Windows
1. open powershell
2. `cd` to this directory
3. `pip install -r requirements.txt`
4. `python3 run.py migrate`
## Linux/MacOS
1. open bash/zsh
2. `cd` to this directory
3. `pip install -r requirements.txt`
4. `python3 run.py migrate`

# Running the solver
1. set up your database.
    * migrate as above
    * export to csv using `python3 run.py dump`
    * make your edits using excel
    * import from csv using `python3 run.py importDump`
2. run `python3 run.py generateRota`