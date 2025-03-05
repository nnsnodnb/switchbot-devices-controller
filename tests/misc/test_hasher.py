import base64
from collections.abc import Generator

import pytest

from misc.hasher import get_b64encoded_digest


class TestGetB64encodedDigest:
    @pytest.fixture
    def data(self) -> Generator[bytes]:
        data = b"test???test"
        yield data
        assert b"/" in base64.b64encode(data)  # check if the data contains a slash

    def test_it(self, data: bytes) -> None:
        actual = get_b64encoded_digest(data)

        assert "/" not in actual
