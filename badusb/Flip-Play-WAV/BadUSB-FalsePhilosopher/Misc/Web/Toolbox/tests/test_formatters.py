import pytest
from toolbox.server.formatters import pretty_date
from datetime import datetime, timedelta

NOW = datetime(2019, 4, 13)


@pytest.mark.parametrize(
    "date,expected",
    [
        (NOW, "0 seconds ago"),
        (NOW - timedelta(seconds=10), "10 seconds ago"),
        (NOW - timedelta(seconds=59), "59 seconds ago"),
        (NOW - timedelta(seconds=60), "1 minutes ago"),
        (NOW - timedelta(seconds=90), "1 minutes ago"),
        (NOW - timedelta(seconds=120), "2 minutes ago"),
        (NOW - timedelta(minutes=59, seconds=59), "59 minutes ago"),
        (NOW - timedelta(minutes=61), "1 hours ago"),
        (NOW - timedelta(minutes=140), "2 hours ago"),
        (NOW - timedelta(weeks=2), "14 days ago"),
    ],
)
def test_upload_token_creation_missing_csrf_token(date, expected):
    assert pretty_date(date, now=NOW) == expected
