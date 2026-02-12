"""Test the structured exception hierarchy."""

from flowscout.core.errors import (
    ActionExecutionError,
    ActionTimeoutError,
    BacktrackFailed,
    BrowserError,
    ConfigError,
    DiscoveryError,
    FlowscoutError,
    MigrationError,
    NavigationError,
    StateCaptureFailed,
    StorageError,
)


class TestHierarchy:
    """Verify isinstance chains work as expected."""

    def test_all_derive_from_flowscout_error(self) -> None:
        for cls in (
            BrowserError,
            NavigationError,
            ActionExecutionError,
            ActionTimeoutError,
            StateCaptureFailed,
            BacktrackFailed,
            StorageError,
            MigrationError,
            DiscoveryError,
            ConfigError,
        ):
            assert issubclass(cls, FlowscoutError)

    def test_browser_subtypes(self) -> None:
        assert issubclass(NavigationError, BrowserError)
        assert issubclass(ActionExecutionError, BrowserError)
        assert issubclass(ActionTimeoutError, ActionExecutionError)
        assert issubclass(StateCaptureFailed, BrowserError)
        assert issubclass(BacktrackFailed, BrowserError)

    def test_storage_subtypes(self) -> None:
        assert issubclass(MigrationError, StorageError)

    def test_catch_flowscout_error_catches_subtypes(self) -> None:
        try:
            raise ActionTimeoutError("timed out")
        except FlowscoutError:
            pass  # Expected

    def test_catch_browser_error_does_not_catch_storage(self) -> None:
        try:
            raise MigrationError("bad migration")
        except BrowserError:
            raise AssertionError("BrowserError should not catch MigrationError")
        except StorageError:
            pass  # Expected

    def test_message_preserved(self) -> None:
        err = ActionTimeoutError("click timed out after 5000ms")
        assert str(err) == "click timed out after 5000ms"
