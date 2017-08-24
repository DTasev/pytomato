This is a Pomodoro timer implementation to be used primarily through the command line. It currently uses `git` to store the entires.

The entires are stored in a configured `git` repository, which has to be changed in [`conf.py`](https://github.com/DTasev/pytomato/blob/master/pytomato/conf.py). Alternatively any backup cloud storage can be used (Google Drive, OneDrive, etc) by adjusting the project directory in the `conf.py` file.

This has been mostly tested with having `git credentials` set up, i.e. you do not need to re-enter your username and password on every push. It needs further testing to properly work with entering credentials and it will probably be fixed the next time I work on a Linux-based workstation.

---

[What is Pomodoro?](https://en.wikipedia.org/wiki/Pomodoro_Technique)

Briefly (from Wikipedia): The technique uses a timer to break down work into intervals, traditionally 25 minutes in length, separated by short breaks. These intervals are named pomodoros, the plural in English of the Italian word pomodoro (tomato), after the tomato-shaped kitchen timer that Cirillo used as a university student.