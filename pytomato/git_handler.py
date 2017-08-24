import datetime
import os
import subprocess
from typing import List, Union

from pytomato.conf import GIT_PUSH_OUTPUT_FILE, REMOTE_UPDATE_TIMEOUT


def is_git_repository(directory):
    return os.path.isdir(os.path.join(directory, ".git"))


def _prep_args(git_exec, args, not_split_args):
    if isinstance(args, str):
        args = args.split(" ")

    args = [git_exec] + args
    if not_split_args:
        args.append(not_split_args)

    return args


def _run(git_exec, args: Union[List[str], str], not_split_args=None) -> subprocess.CompletedProcess:
    args = _prep_args(git_exec, args, not_split_args)
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def _run_detached(git_exec, args: Union[List[str], str], not_split_args=None) -> subprocess.CompletedProcess:
    args = _prep_args(git_exec, args, not_split_args)
    output_file = open(GIT_PUSH_OUTPUT_FILE, 'wb')
    return subprocess.run(args, stdout=output_file, stderr=output_file, shell=True)


class GitHandler(object):
    def __init__(self, git, repo_location, repo_remote_uri, force_upload):
        """
        :parma git: The git executable command or path
        :param repo_location: Path to the local repository
        :param repo_remote_uri: The URI of the remote repository
        :param force_upload: Force an upload to the remote storage at the end of the run
        """
        self.git = Git(git)
        self.repo_location = repo_location
        self.repo_remote_uri = repo_remote_uri
        self.force_upload = force_upload

    def init(self):
        cwd = os.getcwd()
        os.chdir(self.repo_location)
        if not is_git_repository(self.repo_location):
            # try git cloning the remote URI if uri specified and exists
            self.git.init()

        if self.repo_remote_uri:
            print("Pulling remote entries")
            self.git.set_remote(self.repo_remote_uri)
            self.git.pull()

        os.chdir(cwd)

    def upload(self, message) -> int:
        """
        TODO: This needs to be done async, result should be saved in the 
        repo_location and shown to the user on next startup?

        :param message: Message to be used for the commit
        :returns: On success 0, on failure 1
        """
        # change dir without returning because we're exiting
        os.chdir(self.repo_location)

        self.git.add()
        self.git.commit(message)

        if self.is_it_time_to_push():
            self.git.push()
        return 0

    def is_it_time_to_push(self):
        # if remote repository is not set dont push, even if upload is specified
        if self.repo_remote_uri == "":
            return False

        output_file = os.path.join(self.repo_location, GIT_PUSH_OUTPUT_FILE)

        # if forcing upload or no previous output push to remote
        if self.force_upload or not os.path.isfile(output_file):
            return True

        last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(output_file))
        minimum_duration = datetime.timedelta(seconds=REMOTE_UPDATE_TIMEOUT)
        duration_since_last_mod = datetime.datetime.now() - last_mod
        # if previous output exists, check if last modified > config duration
        if duration_since_last_mod > minimum_duration:
            # clear the last output, necessary?
            os.remove(output_file)
            return True

        # finally, file exists, but it has been modified within the specified duration
        return False


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
            print("stdout:", res.stdout.decode())
        if res.returncode != 0:
            if res.stderr:
                print("stderr:", res.stderr.decode())
        return res.returncode

    def init(self):
        if self.git == "":
            return 1
        res = _run(self.git, "init")
        return self._handle_error(res)

    def add(self):
        if self.git == "":
            return 1
        res = _run(self.git, "add .")
        return self._handle_error(res)

    def commit(self, message):
        if self.git == "":
            return 1
        res = _run(self.git, "commit -m", message)
        return self._handle_error(res)

    def set_remote(self, remote_uri):
        if self.git == "":
            return 1
        res = _run(self.git, "remote add origin", remote_uri)
        return self._handle_error(res)

    def clone(self, remote_uri):
        if self.git == "":
            return 1
        res = _run(self.git, ["clone", remote_uri], " . ")
        return self._handle_error(res)

    def push(self):
        if self.git == "":
            return 1
        print("Uploading files to remote repository.")
        _run_detached(self.git, "push --set-upstream origin master")

    def status(self):
        if self.git == "":
            return 1
        res = _run(self.git, "status")
        return self._handle_error(res)

    def branch_track_master(self):
        if self.git == "":
            return 1
        res = _run(self.git, R"branch --set-upstream-to=origin/master master")
        return self._handle_error(res)

    def pull(self):
        if self.git == "":
            return 1
        res = _run(self.git, "pull origin master")
        return self._handle_error(res)
