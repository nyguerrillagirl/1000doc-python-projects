import pytest
from domain import User, Request
from messy import process_request


# --- Helpers ---------------------------------------------------------------

def make_user(
    name="TestUser",
    is_active=True,
    roles=None,
    has_mfa=True,
    subscription_tier="pro",
):
    return User(
        name=name,
        is_active=is_active,
        roles=roles or set(),
        has_mfa=has_mfa,
        subscription_tier=subscription_tier,
    )


def make_request(
    path="/resource",
    action="read",
    requires_audit=False,
    required_role=None,
):
    return Request(
        path=path,
        action=action,
        requires_audit=requires_audit,
        required_role=required_role,
    )


# --- Tests ----------------------------------------------------------------


def test_inactive_user_raises_permission_error():
    user = make_user(is_active=False)
    request = make_request()

    with pytest.raises(PermissionError):
        process_request(user, request)


def test_delete_action_without_mfa_raises_permission_error():
    user = make_user(has_mfa=False)
    request = make_request(action="delete")

    with pytest.raises(PermissionError):
        process_request(user, request)


def test_missing_required_role_raises_permission_error():
    user = make_user(roles={"viewer"})
    request = make_request(required_role="admin")

    with pytest.raises(PermissionError):
        process_request(user, request)


def test_audit_log_is_written_when_required():
    user = make_user(name="Arjan")
    request = make_request(
        action="delete",
        path="/admin/users",
        requires_audit=True,
        required_role=None,
    )

    result = process_request(user, request)

    assert len(result.audit_log) == 1
    assert "Arjan performed delete on /admin/users" in result.audit_log[0]


def test_access_granted_is_set_to_true():
    user = make_user(roles={"admin"})
    request = make_request(required_role="admin")

    result = process_request(user, request)

    assert result.access_granted is True


def test_returns_same_request_object():
    user = make_user(roles={"admin"})
    request = make_request(required_role="admin")

    result = process_request(user, request)

    assert result is request
