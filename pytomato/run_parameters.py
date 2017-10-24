from pytomato.conf import DEFAULT_TOMATO_NAME, SHORT_TOMATO_DURATION, DEFAULT_PROJECT_NAME


class RunParameters:
    run_type = ""
    name = DEFAULT_TOMATO_NAME
    duration = SHORT_TOMATO_DURATION
    clean = False
    list_and_exit = False
    delete = None
    project_name = DEFAULT_PROJECT_NAME
    mute = False
    force_upload = False
