from fastapi import Header, HTTPException
import uuid

class User:
    def __init__(self, id: uuid.UUID, username: str, email: str, display_name: str = None):
        self.id = id
        self.username = username
        self.email = email
        self.display_name = display_name

def get_current_user(x_test_user: str = Header(None)):
    if x_test_user:
        return User(id=uuid.UUID(x_test_user), username="testuser", email="test@example.com")
    raise HTTPException(status_code=401, detail="Not authenticated")
