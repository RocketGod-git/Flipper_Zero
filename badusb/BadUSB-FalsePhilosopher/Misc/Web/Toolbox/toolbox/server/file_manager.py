from contextlib import contextmanager
from pathlib import Path


class InvalidFilePath(Exception):
    pass


class InvalidFilePermissions(Exception):
    pass


class FileManager:
    """
    A file manager that can read and write files. Ensures that no
    arbitrary reads or writes can happen to anywhere other than
    the intended paths. All file interactions should happen via
    an instance of this object.
    """

    def __init__(self, root_user_directory: Path, root_toolbox_directory: Path):
        self.root_user_directory = Path(root_user_directory)
        self.root_toolbox_directory = Path(root_toolbox_directory)

    @contextmanager
    def open_user_file(self, path, mode):
        if not self.is_allowed_user_file_path(path):
            raise InvalidFilePath

        with open(path, mode) as f:
            yield f

    @contextmanager
    def open_toolbox_file(self, path, mode="r"):
        if not self.is_allowed_toolbox_file_path(path):
            raise InvalidFilePath

        if not (mode == "r" or "rb"):
            raise InvalidFilePermissions

        with open(path, mode) as f:
            yield f

    def is_allowed_user_file_path(self, local_path):
        return (
            self.root_user_directory in local_path.resolve().parents
            or self.root_user_directory == local_path
        )

    def is_allowed_toolbox_file_path(self, local_path):
        return (
            self.root_toolbox_directory in local_path.resolve().parents
            or self.root_toolbox_directory == local_path
        )
