from backend.db.models.user import User
from sqlalchemy.orm import Session


def add_profile(save_name: str, current_user: User, db: Session):
    """
    Adds a new profile to the database.
    @param save_name: string name of the profile
    @param current_user: current user
    @param db: database session
    @return: saved profile
    """
    current_user.profile = save_name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


def read_profile(owner: User):
    """
    read and display the profile from the database.
    @param owner: owner of the profile
    @return: retrieved profile
    """
    profile = owner.profile
    if profile is not None:
        with open(owner.profile, "rb") as image:
            image.read()
    else:
        profile = None

    return profile
