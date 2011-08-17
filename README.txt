Made by Entrity.

To use this package, just stick to a few classes, just a few steps. (See more detailed instructions beneath the list.)

1. Download list of subscribers via Streamsend's website (use web browser; this can't be done w/ API).
2. Run 'setup.py' as main module
3. Alter contents of 'data/blast.xml' to correspond to attributes of this email blast (subject line, email id)
4. Run 'schedule.py' as main module
* Wait 1 week so that all scheduled email blasts will complete.
5. Run 'cleanup.py' as main module.
6. Run 'analyze.py' as main module to find what hours of the week returned the best view results for the email blast

* The first time you use this utility, you'll need to make a "_config.py" file and a "data/blast.xml" file (see _sample_config.py and data/sample_blast.xml).
 (You'll need your login id and api key from Streamsend.  Login at Streamsend; go to Account.)

###########################################################
1. download subscribers list
###########################################################
- login to streamsend via their website
- navigate to download/export users (http://app.streamsend.com/audience/1/exports/new)
- check only the box for "Active" under "Opt-Status".
- check only the box for list "Wholesale Customers" under "My Subscribers".
- click "Download Latest Export"
- move the downloaded file to the location specified in '_config.py' as 'SUBSCRIBERS_FILE' (default is '/data/My Subscribers.txt')

###########################################################
2. setup
###########################################################
- randomly divides subscribers into 168 groups of equal size
- writes groups to individual files in directory specified by _config.DIR_OF_USER_LISTS
- creates 168 lists on streamsend
- uploads groups' files to streamsend
- imports each group file to one of the 168 lists on streamsend
- creates files data/168-user-lists/*.txt (just for diagnostics)
- creates file list_ids.csv (used for steps 4-6)

###########################################################
4. schedule
###########################################################
- queries user for the id of an email on streamsend
- schedules a blast for that email for each of the lists created in step 2

###########################################################
5. cleanup
###########################################################
- deletes the 168 lists from streamsend

###########################################################
6. analyze
###########################################################
- when prompted, enter the filename (it should be a timestamp) of the file containing a list of blasts you wish you analyze (directory should be data/blast-ids)
- gets blast ids from a given csv file in data/
- gets views for each
- read the analysis in data/analysis/[timestamp]-views.txt