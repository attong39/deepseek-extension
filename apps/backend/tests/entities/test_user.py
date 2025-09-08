"""Test User entity with normalization."""

from apps.backend.core.domain.entities.user import User, UserRole


def test_user_lifecycle_and_permissions():
    """Test user lifecycle and permission management."""
    u = User(id="u1", email="A@B.Com", display_name="A")
    assert u.is_active
    assert u.email == "a@b.com"  # normalized
    assert UserRole.USER in u.roles

    u2 = (
        u.add_roles(UserRole.ADMIN)
        .grant("read:any", "write:own", "Read:Any")
        .deactivate()
    )
    assert not u2.is_active
    assert u2.has_role(UserRole.ADMIN)
    assert u2.has_perm("read:any")
    assert "read:any" in u2.permissions and "write:own" in u2.permissions
    # dedupe + lower
    assert u2.permissions == ["read:any", "write:own"]

    u3 = u2.revoke("write:own").activate()
    assert u3.is_active
    assert not u3.has_perm("write:own")


def test_user_email_normalization():
    """Test email normalization."""
    u = User(id="u1", email="TEST@EXAMPLE.COM")
    assert u.email == "test@example.com"


def test_user_permissions_normalization():
    """Test permissions normalization."""
    # Test list input with duplicates and mixed case
    u = User(
        id="u1",
        email="test@test.com",
        permissions=["READ:any", "read:any", "Write:Own"],
    )
    assert u.permissions == ["read:any", "write:own"]


def test_user_role_management():
    """Test role addition and removal."""
    u = User(id="u1", email="test@test.com")

    # Add roles
    u2 = u.add_roles(UserRole.ADMIN, UserRole.VIEWER)
    assert UserRole.ADMIN in u2.roles
    assert UserRole.VIEWER in u2.roles
    assert UserRole.USER in u2.roles  # default role preserved

    # Remove roles
    u3 = u2.remove_roles(UserRole.USER)
    assert UserRole.USER not in u3.roles
    assert UserRole.ADMIN in u3.roles  # other roles preserved


def test_user_immutability():
    """Test that user is immutable."""
    u = User(id="u1", email="test@test.com")

    # Test activation returns new instance
    u2 = u.deactivate()
    assert u.is_active
    assert not u2.is_active

    # Test role changes return new instance
    u3 = u.add_roles(UserRole.ADMIN)
    assert UserRole.ADMIN not in u.roles
    assert UserRole.ADMIN in u3.roles


def test_user_permission_helpers():
    """Test permission helper methods."""
    u = User(id="u1", email="test@test.com", permissions=["read:any", "write:own"])

    assert u.has_perm("read:any")
    assert u.has_perm("READ:ANY")  # case insensitive
    assert u.has_perm("Write:Own")  # case insensitive
    assert not u.has_perm("delete:any")


def test_user_preferences():
    """Test user preferences handling."""
    prefs = {"theme": "dark", "language": "en"}
    u = User(id="u1", email="test@test.com", preferences=prefs)
    assert u.preferences == prefs


def test_user_touch_updates_timestamp():
    """Test that touch() updates the timestamp."""
    u = User(id="u1", email="test@test.com")
    original_time = u.updated_at

    u2 = u.touch()
    assert u2.updated_at >= original_time
    assert u.updated_at == original_time  # original unchanged
