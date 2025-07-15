from models.admin import Admin


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def get_admin(username: str) -> Admin:
    admin = await Admin.find_one(Admin.username == username)
    return admin
