# 25 minutes
DEFAULT_SHORT_TOMATO_DURATION = 1500

# 50 minutes
DEFAULT_LONG_TOMATO_DURATION = 3000

# 5 minutes
DEFAULT_SHORT_BREAK_DURATION = 300

# 10 minutes
DEFAULT_LONG_BREAK_DURATION = 600

DEFAULT_TOMATO_NAME = "Tomato"
DEFAULT_BREAK_NAME = "Tomato Break"

DEFAULT_TOMATO_TYPE = "Tomato"
DEFAULT_BREAK_TYPE = "Break"


class DefaultRun:
    runType = None
    name = DEFAULT_TOMATO_NAME
    duration = DEFAULT_SHORT_TOMATO_DURATION
    clean = False
    listAndExit = False
    delete = None
