import os
import subprocess

from typing import List, Union


def isGitRepository(directory):
    return os.path.isdir(os.path.join(directory, ".git"))


def _run(args: Union[List[str], str], not_split_args="") -> subprocess.CompletedProcess:
    if isinstance(args, str):
        args = args.split(" ")

    args += not_split_args

    # TODO remove the shell and run without, need to catch FileNotFoundError exception
    # if the git executable is not found
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


class Git(object):
    """
    Naive Git implementation to directly use it through the shell
    """

    def __init__(self, git="git"):
        """
        :param git: Specify the location of the git executable. 
                    Default is just "git", which requires git to be on the PATH
        """
        self.git = git

    def init(self):
        res = _run(self.git + " init")
        if res.returncode != 0:
            return 0

    def add(self):
        res = _run(self.git + " add .")
        if res.returncode != 0:
            return 0

    def commit(self, message):
        res = _run(self.git + " commit -m ", message)
        if res.returncode != 0:
            return 0
