import os
import subprocess

from typing import List, Union

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200


def is_git_repository(directory):
    return os.path.isdir(os.path.join(directory, ".git"))


def _run(args: Union[List[str], str], not_split_args=None) -> subprocess.CompletedProcess:
    if isinstance(args, str):
        args = args.split(" ")

    if not_split_args:
        args.append(not_split_args)

    # TODO remove the shell and run without, need to catch FileNotFoundError exception
    # if the git executable is not found
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def _run_detached(args: Union[List[str], str], not_split_args=None) -> subprocess.CompletedProcess:
    if isinstance(args, str):
        args = args.split(" ")

    if not_split_args:
        args.append(not_split_args)

    output_file = open('last_output.out', 'wb')
    return subprocess.run(args, stdout=output_file, stderr=output_file, shell=True)


class GitHandler(object):
    def __init__(self, git, repo_location, repo_remote_uri):
        self.git = Git(git)
        self.repo_location = repo_location
        self.repo_remote_uri = repo_remote_uri

    def upload(self, message) -> int:
        """
        TODO: This needs to be done async, result should be saved in the repo_location and shown to the user on next startup?
        :returns: On success 0, on failure 1
        """
        os.chdir(self.repo_location)

        self.git.init()

        self.git.add()
        self.git.commit(message)

        self.git.set_remote(self.repo_remote_uri)
        self.git.push()
        return 0


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

    def _handle_error(self, res):
        if res.stdout:
            print(res.stdout.decode())
        if res.returncode != 0:
            if res.stderr:
                print(res.stderr.decode())
        return res.returncode

    def init(self):
        res = _run(self.git + " init")
        return self._handle_error(res)

    def add(self):
        res = _run(self.git + " add .")
        return self._handle_error(res)

    def commit(self, message):
        res = _run(self.git + " commit -m", message)
        return self._handle_error(res)

    def set_remote(self, remote_uri):
        res = _run(self.git + " remote add origin", remote_uri)
        return self._handle_error(res)

    def clone(self, remote_uri):
        res = _run(self.git + " clone", remote_uri)
        return self._handle_error(res)

    def push(self):
        print("Uploading files to remote repository.")
        _run_detached(self.git + " push --set-upstream origin master")

    def status(self):
        res = _run(self.git + " status")
        return self._handle_error(res)

    def pull(self):
        res = _run(self.git + " pull origin master")
        return self._handle_error(res)
