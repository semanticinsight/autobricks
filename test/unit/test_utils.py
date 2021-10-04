import sys
from pytest_mock import mocker
from autobricks import DecodeUtils

def test_base64_decode_utf8():

    result = DecodeUtils.base64_decode("SGVsbG8gV29ybGQ=").decode("utf-8")

    assert result == "Hello World"


def test_base64_encode_utf8():

    result = DecodeUtils.base64_encode("Hello World".encode("utf-8"))

    assert result == "SGVsbG8gV29ybGQ="


def test_base64_decode_ascii():

    encoding = "ascii"
    result = DecodeUtils.base64_decode("SGVsbG8gV29ybGQ=", encoding).decode(encoding)

    assert result == "Hello World"


def test_base64_encode_ascii():

    encoding = "ascii"
    result = DecodeUtils.base64_encode("Hello World".encode(encoding), encoding)

    assert result == "SGVsbG8gV29ybGQ="


def test_post_data():

    mocker.patch.object(sys, "platform", "linux")

    assert not DecodeUtils.is_windows()


def test_post_data(mocker):

    mocker.patch.object(sys, "platform", "win32")

    assert DecodeUtils.is_windows()


def test_format_linux_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for_os("/not/a/windows/path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_part_linux_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for_os("/not/a\\windows/path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_win32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for_os("\\not\\a\\windows\\path")
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for_os("\\not\\a\\linux\\path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_part_win32_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for_os("\\not\\a/linux\\path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_linux_path_for_linux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for_os("/not/a/linux/path")
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_win32_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for_os("\\not\\a\\darwin\\path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_part_win32_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for_os("\\not\\a/darwin\\path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_darwin_path_for_darwin(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for_os("/not/a/darwin/path")
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_linux_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for("/not/a/windows/path", DecodeUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_part_linux_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for("/not/a\\windows/path", DecodeUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_oswin32(mocker):

    mocker.patch.object(sys, "platform", "win32")
    result = DecodeUtils.format_path_for("\\not\\a\\windows\\path", DecodeUtils.OS.WINDOWS)
    expected = "\\not\\a\\windows\\path"

    assert result == expected


def test_format_win32_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for("\\not\\a\\linux\\path", DecodeUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_part_win32_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for("\\not\\a/linux\\path", DecodeUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_linux_path_for_oslinux(mocker):

    mocker.patch.object(sys, "platform", "linux")
    result = DecodeUtils.format_path_for("/not/a/linux/path", DecodeUtils.OS.LINUX)
    expected = "/not/a/linux/path"

    assert result == expected


def test_format_win32_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for("\\not\\a\\darwin\\path", DecodeUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_part_win32_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for("\\not\\a/darwin\\path", DecodeUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_linux_path_for_osmac(mocker):

    mocker.patch.object(sys, "platform", "darwin")
    result = DecodeUtils.format_path_for("/not/a/darwin/path", DecodeUtils.OS.MAC)
    expected = "/not/a/darwin/path"

    assert result == expected


def test_format_exception(mocker):

    path = "/not/a/darwin/path"
    osystem = "superduperos"
    mocker.patch.object(sys, "platform", osystem)

    expected = (
        f"Error formating path={path} for os. Operating system not supported {osystem}"
    )

    error_message = None
    try:
        result = DecodeUtils.format_path_for_os(path)

    except Exception as e:
        error_message = str(e)

    assert error_message == expected


def test_is_windows(mocker):

    mocker.patch.object(sys, "platform", "win32")
    assert DecodeUtils.is_windows()


def test_is_not_windows(mocker):

    mocker.patch.object(sys, "platform", "linux")
    assert not DecodeUtils.is_windows()
