import os

# Duration of a short Tomato run, default 1500 seconds (25 minutes)
SHORT_TOMATO_DURATION = 1500

# Duration of a long Tomato run, default 3000 seconds (50 minutes)
LONG_TOMATO_DURATION = 3000

# Duration of a short break, default 300 seconds (5 minutes)
SHORT_BREAK_DURATION = 300

# Duration of a long break, default 600 seconds (10 minutes)
LONG_BREAK_DURATION = 600

# Default entry name for a Tomato run
DEFAULT_TOMATO_NAME = "Tomato"

# Default entry name for a break run
DEFAULT_BREAK_NAME = "Tomato Break"

# Used by the scripts to separate work 'tomato' runs with break runs
# I don't see a reason to change this, but maybe someone doesn't like tomatoes
TOMATO_TYPE = "Tomato"
BREAK_TYPE = "Break"

# Directory where the tomato proejct files will be stored.
PYTOMATO_PROJECTS_DIR = os.path.expanduser("~/pytomato_entries")

# Default name of the project used for entries without a custom project specified
DEFAULT_PROJECT_NAME = "default"

# The extension of the file.
PROJECT_EXTENSION = ".tomato"

# Git executable that will be used to run the git commands. 
# This can be a full path to the git executable such as C:\Program Files\Git\git.exe
# Just keep the R in front so that python reads it as a literal string
GIT_EXECUTABLE_PATH = R"git"

# The repository used for storing the entry files.
# The one already here is a test repostitory and you won't have push access to it.
GIT_REMOTE_REPOSITORY_URI = "https://github.com/dtasev/pytomato_entries"
GIT_PUSH_OUTPUT_FILE = "git_push.out"

# Minimum duration before pushing any changes to the remote. 
# Default is 1800 seconds (30 minutes)
REMOTE_UPDATE_TIMEOUT = 1800
