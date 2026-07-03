import os 

#Directory to monitor
WATCH_DIRECTORY = os.path.expanduser("~/test_directory")

#DATABASE FILE = stores baseline and logs
DATABASE_PATH = "fim.db"

#LOG_FILE = human readable log events
LOG_PATH = "fim.log"

#checking interval 
CHECK_INTERVAL = 1

#ALERT 
ALERT_LEVELS = {
                 "created": "warning",
                 "modified": "CRITICAL",
                 "deleted": "critical"
}


HMAC_SECRET_KEY = "ef285b1acfd0f0d70a3e2a9ea677ed4b093da2803594f720a470f80f9b3865df"
