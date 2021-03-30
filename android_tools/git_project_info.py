class GitProjectInfo:
    """
    describe a git repository, contains git repository name, revision,
    and where to clone to.

    diff id name diff file name requires if for diff patch.
    """

    def __init__(self, path, git_name, git_revision, user_name, diff_id=None, diff_name=None):
        """
        Args:
            path: git repository cloned to
            git_name: git repository name
            git_revision: git revision
            diff_id: create diff with this id
            diff_name: create diff patch with this name
        """
        self._path = path
        self._git_ssh = 'ssh://'
        self._git_user = user_name
        self._git_ip = '@10.20.40.21:29418/'
        self._git_url_prefix = ''.join([self._git_ssh, self._git_user, self._git_ip])
        self._url = self._git_url_prefix + git_name
        self._revision = git_revision
        self._diff_id = diff_id
        self._diff_name = diff_name

    def __str__(self):
        return "git clone {}, " \
               "to {}, " \
               "with revision {}, " \
               "diff id {}, " \
               "diff file name {}." \
            .format(self._url, self._path, self._revision, self._diff_id, self._diff_name)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._path = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._url = value

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._revision = value

    @property
    def user_name(self):
        return self._git_user

    @user_name.setter
    def user_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._git_user = value

    @property
    def diff_id(self):
        return self._diff_id

    @diff_id.setter
    def diff_id(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._diff_id = value

    @property
    def diff_name(self):
        return self._diff_name

    @diff_name.setter
    def diff_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._diff_name = value
