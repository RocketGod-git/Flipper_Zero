from flask import (
    Blueprint,
    Flask,
    render_template,
    make_response,
    app,
    current_app,
    request,
    redirect,
    url_for,
)
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json
from pathlib import Path
from typing import List, Mapping, Union
from .payload_generator import PayloadGenerator
from .file_manager import FileManager
from datetime import datetime

ServerPath = str
LocalPath = Path
ServerPathMap = Mapping[ServerPath, LocalPath]
Bytes = int


@dataclass
class ServerDirectoryItem:
    server_path: ServerPath
    name: str
    modified_at: str
    size: Bytes
    is_dir: str
    is_file: str


@dataclass
class ServerInvalidFilePath:
    pass


@dataclass
class ServerDirectoryListing:
    user_files: List[ServerDirectoryItem]
    toolbox_files: List[ServerDirectoryItem]
    server_path: ServerPath


@dataclass
class ServerFileResult:
    local_path: LocalPath
    content: bytes


ServerResponse = Union[ServerInvalidFilePath, ServerDirectoryListing, ServerFileResult]


def as_server_directory_item(server_path, local_path) -> ServerDirectoryItem:
    stat = local_path.stat()
    return ServerDirectoryItem(
        server_path=server_path,
        name=Path(server_path).name,
        modified_at=datetime.fromtimestamp(stat.st_mtime),
        size=stat.st_size,
        is_dir=local_path.is_dir(),
        is_file=local_path.is_file(),
    )


class ServerConfig:
    def __init__(
        self, root_toolbox_directory: str, config_path: str, file_manager: FileManager
    ):
        self.root_toolbox_directory = root_toolbox_directory
        self.file_manager: FileManager = file_manager
        self.server_files: ServerPathMap = self._parse_config(config_path)

    def get_local_path(self, server_path: ServerPath) -> Optional[LocalPath]:
        return self.server_files.get(server_path, None)

    def items(self):
        return self.server_files.items()

    def server_paths(self) -> List[ServerPath]:
        return self.server_files.keys()

    def _parse_config(self, config_path: str) -> ServerPathMap:
        server_files = {}
        with self.file_manager.open_toolbox_file(config_path) as config_file:
            config = json.load(config_file)

        for config_value in config["server"]:
            server_path = config_value["server_path"]
            local_path = config_value["local_path"]
            if server_path in server_files:
                raise ValueError(
                    f"Duplicate server_path '{server_path}' for local_path '{local_path}'"
                )
            local_path = self.root_toolbox_directory / local_path
            if not local_path.exists():
                raise ValueError(f"local_path '{local_path}' does not exist.")

            server_files[server_path] = Path(local_path)
        return server_files


def removeprefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix) :]
    else:
        return self[:]


class UserFileServer:
    def __init__(self, server_config: ServerConfig):
        self.server_config = server_config
        self.file_manager = server_config.file_manager

    def serve_user_file_or_folder(self, server_path: ServerPath):
        """
        Serve a file or folder from user specified files

        If the given file or folder does not exist, a 404 is returned
        """
        root_user_directory = Path(current_app.config["ROOT_USER_DIRECTORY"])
        local_path = (root_user_directory / server_path).resolve()

        def calculate_file_server_path_func(file_path: Path) -> ServerPath:
            return f"/{file_path.relative_to(root_user_directory).as_posix()}"

        return self._serve_file_or_folder(
            local_path, server_path, calculate_file_server_path_func
        )

    # TODO: Split out user / toolbox files, this does both currently
    def _serve_file_or_folder(
        self,
        local_path: LocalPath,
        server_path: ServerPath,
        calculate_file_server_path_func,
    ) -> ServerResponse:
        """
        Attempts to serve the given file or directory to the user.

        If the local_path is a file, it sends a file to the user.
        If the local_path is a folder, it renders the directory contents

        To guard against arbitrary reads - the local_path must exist within the
        restrict_to_path argument, otherwise a ServerInvalidFilePath object is returned.
        """

        valid_child_path = (
            self.file_manager.is_allowed_user_file_path(local_path)
        ) and local_path.exists()
        if not valid_child_path:
            return ServerInvalidFilePath()

        if local_path.is_file():
            return self._read_user_file(local_path)
        elif local_path.is_dir():
            files = []
            for child_path in local_path.iterdir():
                files.append(
                    as_server_directory_item(
                        server_path=calculate_file_server_path_func(child_path),
                        local_path=child_path,
                    )
                )
            files.sort(key=lambda file: file.name)

            return ServerDirectoryListing(
                user_files=files,
                toolbox_files=self._get_toolbox_files(),
                server_path=server_path,
            )
        else:
            return ServerInvalidFilePath()

    def _get_toolbox_files(self) -> List[ServerDirectoryItem]:
        toolbox_files = []
        for server_path, local_path in self.server_config.items():
            toolbox_files.append(
                as_server_directory_item(server_path=server_path, local_path=local_path)
            )
        toolbox_files.sort(key=lambda file: file.name)
        return toolbox_files

    def _read_user_file(self, local_path: LocalPath):
        """
        Responds with the current file if it exists as a file
        """
        is_valid_path = (
            self.file_manager.is_allowed_user_file_path(local_path)
            and local_path.exists()
            and local_path.is_file()
        )
        if not is_valid_path:
            return ServerInvalidFilePath()

        with self.file_manager.open_user_file(local_path, "rb") as file:
            content = file.read()
            return ServerFileResult(local_path=local_path, content=content)

        return ServerInvalidFilePath()


class ToolboxFileServer:
    def __init__(self, server_config: ServerConfig):
        self.server_config = server_config
        self.file_manager = server_config.file_manager

    def serve_toolbox_file_or_folder(self, server_path: ServerPath):
        """
        Serve an inbuilt / custom configured file or folder.

        If the given file or folder does not exist, None is returned
        """
        # First test if the file can be found as a direct mapping
        server_path_namespace = None
        local_path_mapping = self.server_config.get_local_path("/" + server_path)

        # There may not be a local file found, but test if it exists as a namespace
        if local_path_mapping is None:
            server_path_namespace = server_path.split("/")[0]
            local_path_mapping = self.server_config.get_local_path(
                "/" + server_path_namespace
            )

        if local_path_mapping is None:
            return None

        local_path = None
        if server_path_namespace is None:
            local_path = local_path_mapping
        else:
            relative_path = removeprefix(server_path, server_path_namespace)
            if relative_path[0] == "/":
                relative_path = relative_path[1:]
            local_path = (local_path_mapping / relative_path).resolve()

        def calculate_file_server_path_func(file_path: Path):
            server_path_prefix = None
            if server_path_namespace is None:
                server_path_prefix = f"/{server_path}/"
            else:
                server_path_prefix = f"/{server_path_namespace}/"

            return f"{server_path_prefix}{str(file_path.relative_to(local_path_mapping).as_posix())}"

        return self._serve_file_or_folder(
            local_path,
            server_path,
            calculate_file_server_path_func,
        )

    def _serve_file_or_folder(
        self,
        local_path: LocalPath,
        server_path: ServerPath,
        calculate_file_server_path_func,
    ) -> ServerResponse:
        """
        Attempts to serve the given file or directory to the user.

        If the local_path is a file, it sends a file to the user.
        If the local_path is a folder, it renders the directory contents

        To guard against arbitrary reads - the local_path must exist within the
        restrict_to_path argument, otherwise a ServerInvalidFilePath object is returned.
        """

        valid_child_path = (
            self.file_manager.is_allowed_toolbox_file_path(local_path)
        ) and local_path.exists()
        if not valid_child_path:
            return ServerInvalidFilePath()

        if local_path.is_file():
            return self._read_toolbox_file(local_path)
        elif local_path.is_dir():
            files = []
            for child_path in local_path.iterdir():
                files.append(
                    as_server_directory_item(
                        server_path=calculate_file_server_path_func(child_path),
                        local_path=child_path,
                    )
                )

            return ServerDirectoryListing(
                user_files=files,
                toolbox_files=self._get_toolbox_files(),
                server_path=server_path,
            )
        else:
            return ServerInvalidFilePath()

    def _get_toolbox_files(self) -> List[ServerDirectoryItem]:
        toolbox_files = []
        for server_path, local_path in self.server_config.items():
            toolbox_files.append(
                as_server_directory_item(server_path=server_path, local_path=local_path)
            )

        toolbox_files.sort(key=lambda file: file.name)
        return toolbox_files

    def _read_toolbox_file(self, local_path: LocalPath):
        """
        Responds with the current file if it exists as a file
        """
        is_valid_path = (
            self.file_manager.is_allowed_toolbox_file_path(local_path)
            and local_path.exists()
            and local_path.is_file()
        )
        if not is_valid_path:
            return ServerInvalidFilePath()

        is_allowed_path = any(
            allowed_local_path in local_path.parents or allowed_local_path == local_path
            for _server_path, allowed_local_path in self.server_config.items()
        )
        if not is_allowed_path:
            return ServerInvalidFilePath()

        with self.file_manager.open_toolbox_file(local_path, "rb") as file:
            content = file.read()
            return ServerFileResult(local_path=local_path, content=content)

        return ServerInvalidFilePath()


class FileServer:
    def __init__(self, server_config: ServerConfig):
        self.server_config = server_config
        self.file_manager = server_config.file_manager

    def serve(self, server_path: ServerPath):
        toolbox_file_server = ToolboxFileServer(server_config=self.server_config)
        toolbox_file = toolbox_file_server.serve_toolbox_file_or_folder(server_path)
        if toolbox_file is not None:
            return toolbox_file

        user_file_server = UserFileServer(server_config=self.server_config)
        return user_file_server.serve_user_file_or_folder(server_path)
