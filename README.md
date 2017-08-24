This is a Pomodoro timer implementation to be used primarily through the command line. It currently uses `git` to store the entires.

The entires are stored in a configured `git` repository, which has to be changed in [`conf.py`](https://github.com/DTasev/pytomato/blob/master/pytomato/conf.py). Alternatively any backup cloud storage can be used (Google Drive, OneDrive, etc) by adjusting the project directory in the `conf.py` file.

This has been mostly tested with having `git credentials` set up, i.e. you do not need to re-enter your username and password on every push. It needs further testing to properly work with entering credentials and it will probably be fixed the next time I work on a Linux-based workstation.

---

[What is Pomodoro?](https://en.wikipedia.org/wiki/Pomodoro_Technique)
---------------------------------------------------------------------
Briefly (from Wikipedia): The technique uses a timer to break down work into intervals, traditionally 25 minutes in length, separated by short breaks. These intervals are named pomodoros, the plural in English of the Italian word pomodoro (tomato), after the tomato-shaped kitchen timer that Cirillo used as a university student.

---

How to install `pytomato`?
------------------------

1. You need to have Python 3.6 installed. 
    - To use the GUI notification you also need PyQt5 installed. This can be done by `pip install -r install-requirements.txt`
    - Alternatively, without a GUI notification, you do not need anything else installed.
    - For development install the developer requirements with `pip install -r developer-requirements.txt`
        - The repository has a `settings.json` for the Python VSCode extension to set up default settings for the project.

1. Clone or download the repository

1. Set up the `git` executable and the remote repository in `conf.py`.
    - If not using `git` for storing the entries files, set the `git` executable variable to an empty string `""`.
    - The entries can be stored in cloud drives (OneDrive, Google Drive, etc) by changing the project directory to one of the cloud drives' folders. The files will be automatically synced by the cloud backup system as normal files would.
    
1. Start with `python pytomato` (targetting the top level pytomato, i.e. the one holding the repository files)
    - This will pick up the `__main__.py` file inside and start the timer.
    - Alternatively the timer can be started by doing `python .` inside the repository folder, as will also pick up the `__main__.py` file.
    
1. Without any parameters a default run will be started, lasting 25 minutes with the name Tomato, part of the project `default`. All entries without a custom project will be saved into the `default` one.
    - For the full list of parameters pass the `-h` or `--help` flag.

1. The default durations for short and long runs can be adjusted from the `conf.py` file, along with other settings available, please refer to the file.
