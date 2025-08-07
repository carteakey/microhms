"""
Test cases for basic functionality
"""
import pytest
from project.models import db, User, Role, RoleAssignment


def test_index_page(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200


def test_user_creation():
    """Test user creation functionality."""
    user = User('testuser', 'testpassword', True)
    assert user.username == 'testuser'
    assert user.active == True


def test_role_creation():
    """Test role creation functionality."""
    role = Role('testrole', True)
    assert role.name == 'testrole'
    assert role.active == True


def test_database_models(app):
    """Test that database models work correctly."""
    with app.app_context():
        # Test user creation
        user = User.create('testuser', 'password123')
        assert user.username == 'testuser'
        
        # Test role creation  
        role = Role.create('admin')
        assert role.name == 'admin'
        
        # Test role assignment
        assignment = RoleAssignment.create('admin', user.id)
        assert assignment.role_name == 'admin'
        assert assignment.user_id == user.id