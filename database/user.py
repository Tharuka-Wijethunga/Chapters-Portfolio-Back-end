from models.user import User


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def get_user(email: str) -> User:
    user = await User.find_one(User.email == email)
    return user