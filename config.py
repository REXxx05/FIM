import os 

#Directory to monitor
WATCH_DIRECTORY = os.path.expanduser("~/test_directory)

#DATABASE FILE = stores baseline and logs
DATABASE_PATH = "fim.db"

#LOG_FILE = human readable log events
LOG_PATH - "fim.log"

#checking interval 
CHECK_INTERVAL = 1

#ALERT 
ALERT_LEVELS = {
                 "created": "warning",
                 "modified": "CRITICAL",
                 "deleted": "critical"
}
