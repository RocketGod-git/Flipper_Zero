import pytest
from toolbox.server import server
from pathlib import Path
from flask import Flask
from http import HTTPStatus
import tempfile
import secrets
import pytest
import re
import io
import os
import builtins
from pytest_mock import MockerFixture
from pathlib import Path


def extract_token_id(response, file_name):
    assert response.status_code == HTTPStatus.OK

    match = re.search(
        f'curl -F "file=@{file_name}" -F "token_id=(.*)" http://localhost/uploads',
        response.data.decode("utf-8"),
    )
    assert match is not None

    token_id = match.group(1)
    assert token_id is not None
    return token_id


def test_upload_token_creation(app, client, req_ctx):
    csrf_token = client.get("/csrf_token").data.decode("utf-8")
    response = client.post(
        "/tokens",
        content_type="application/x-www-form-urlencoded",
        data=dict(csrf_token=csrf_token, file_name="test_upload_file.txt"),
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.OK
    assert extract_token_id(response, file_name="./test_upload_file.txt") is not None


@pytest.mark.parametrize(
    "csrf_token,expected_data",
    [
        (None, b"The CSRF token is missing"),
        ("abcdef", b"The CSRF session token is missing"),
    ],
)
def test_upload_token_creation_missing_csrf_token(
    csrf_token, expected_data, app, client, req_ctx
):
    response = client.post(
        "/tokens",
        content_type="application/x-www-form-urlencoded",
        data=dict(csrf_token=csrf_token, file_name="test_upload_file.txt"),
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert expected_data in response.data


def test_upload_file(mocker: MockerFixture, app, client, req_ctx):
    def _mock_open(path, mode):
        if path.name == "config.json":
            return open(path, mode)
        elif path.name == "test_upload_file.txt":
            return tempfile.TemporaryFile(mode)
        else:
            raise "Unexpected scenario"

    mock_open = mocker.Mock()
    mock_open.side_effect = _mock_open

    file_manager_open_stub = mocker.patch("toolbox.server.file_manager.open", mock_open)
    csrf_token = client.get("/csrf_token").data.decode("utf-8")
    response = client.post(
        "/tokens",
        content_type="application/x-www-form-urlencoded",
        data=dict(csrf_token=csrf_token, file_name="test_upload_file.txt"),
        follow_redirects=True,
    )

    token_id = extract_token_id(response, file_name="./test_upload_file.txt")
    new_file_content = b"testing file upload content\n"
    response = client.post(
        "/uploads",
        content_type="multipart/form-data",
        data=dict(
            token_id=token_id,
            file=(io.BytesIO(new_file_content), "test_upload_file.txt"),
        ),
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.data == b'{ "success": true }\n'
    file_manager_open_stub.assert_called_with(
        Path("./tests/harnesses/simple/serve/test_upload_file.txt").resolve(), "wb"
    )


@pytest.mark.parametrize(
    "file_name",
    [
        "../arbitrary_write.txt",
        "/tmp/arbitrary_write.txt",
    ],
)
def test_local_file_inclusion(mocker: MockerFixture, app, client, req_ctx, file_name):
    def _mock_open(path, mode):
        if path.name == "config.json":
            return open(path, mode)
        else:
            raise "Unexpected scenario"

    mock_open = mocker.Mock()
    mock_open.side_effect = _mock_open

    file_manager_open_stub = mocker.patch("toolbox.server.file_manager.open", mock_open)
    csrf_token = client.get("/csrf_token").data.decode("utf-8")
    response = client.post(
        "/tokens",
        content_type="application/x-www-form-urlencoded",
        data=dict(csrf_token=csrf_token, file_name=file_name),
        follow_redirects=True,
    )

    token_id = extract_token_id(response, file_name=f"./{file_name}")
    new_file_content = b"testing file upload content\n"
    response = client.post(
        "/uploads",
        content_type="multipart/form-data",
        data=dict(
            token_id=token_id,
            file=(io.BytesIO(new_file_content), file_name),
        ),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == b'{ "error": "invalid path" }\n'


def test_upload_token_creation_invalid_token(
    mocker: MockerFixture, app, client, req_ctx
):
    file_manager_open_stub = mocker.patch("toolbox.server.file_manager.open")
    new_file_content = b"testing file upload"
    response = client.post(
        "/uploads",
        content_type="multipart/form-data",
        data=dict(
            token_id="invalid_token",
            file=(io.BytesIO(new_file_content), "test_upload_file.txt"),
        ),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == b'{ "error": "token not valid" }\n'
    file_manager_open_stub.assert_not_called()
