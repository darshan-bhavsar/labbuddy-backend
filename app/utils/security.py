from typing import List
from fastapi import Depends, HTTPException, status
from ..models.user import User, UserRole
from .auth import get_current_user


def require_role(allowed_roles: List[UserRole]):
    """Decorator to require specific roles for access."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker


def require_lab_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require lab admin role."""
    if current_user.role != UserRole.LAB_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lab admin access required"
        )
    return current_user


def require_lab_staff(current_user: User = Depends(get_current_user)) -> User:
    """Require lab staff role (admin or staff)."""
    if current_user.role not in [UserRole.LAB_ADMIN, UserRole.LAB_STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lab staff access required"
        )
    return current_user


def require_hospital_user(current_user: User = Depends(get_current_user)) -> User:
    """Require hospital user role."""
    if current_user.role != UserRole.HOSPITAL_USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hospital user access required"
        )
    return current_user
