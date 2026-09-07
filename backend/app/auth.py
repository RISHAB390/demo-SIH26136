from typing import Callable
from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

def get_current_user(
    x_user_id: int | None = Header(None, alias="X-User-Id"),
    db: Session = Depends(get_db)
) -> User:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-User-Id header. Please select a demo user."
        )
    
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {x_user_id} not found."
        )
    return user

def require_role(*allowed_roles: str) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: User role '{current_user.role}' is not authorized. Required: {list(allowed_roles)}"
            )
        return current_user
    return role_checker
