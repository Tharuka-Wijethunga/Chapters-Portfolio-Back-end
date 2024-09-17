from typing import List, Union, Optional
from beanie import PydanticObjectId
from bson import ObjectId

from models.admin import Admin
from models.user import User
from models.student import Student
from models.project import Project, ProjectUpdate



async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def retrieve_students() -> List[Student]:
    students = await Student.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await Student.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await Student.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    student = await Student.get(id)
    if student:
        await student.update(update_query)
        return student
    return False


async def get_admin(username: str) -> Admin:
    admin = await Admin.find_one(Admin.username == username)
    return admin

async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def get_user(email: str) -> User:
    user = await User.find_one(User.email == email)
    return user



async def get_projects(
    name: Optional[str] = None,
    visibility: Optional[bool] = None,
    sort_field: Optional[str] = None,
    sort_direction: str = "ascending",
    page: int = 1,
    page_size: int = 10
) -> List[Project]:
    filter_params = {}
    if name:
        filter_params["name"] = {"$regex": name, "$options": "i"}
    if visibility is not None:
        filter_params["visibility"] = visibility

    sort_params = {}
    if sort_field:
        sort_params[sort_field] = 1 if sort_direction == "ascending" else -1

    skip = (page - 1) * page_size

    projects = await Project.find(filter_params).sort(sort_params).skip(skip).limit(page_size).to_list()
    return projects

async def get_project(id: ObjectId) -> Optional[Project]:
    return await Project.get(id)

async def create_project(project: Project) -> Project:
    return await project.insert()

async def update_project(id: ObjectId, project_update: ProjectUpdate) -> Optional[Project]:
    project = await Project.get(id)
    if project:
        await project.update({"$set": project_update.dict(exclude_unset=True)})
        return project
    return None

async def delete_project(id: ObjectId) -> bool:
    project = await Project.get(id)
    if project:
        await project.delete()
        return True
    return False

async def search_projects(query: str) -> List[Project]:
    projects = await Project.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ],
        "visibility": True
    }).to_list()
    return projects

async def set_featured_status(id: str, featured: bool) -> Optional[Project]:
    project = await Project.get(ObjectId(id))
    if project:
        project.featured = featured
        await project.save()
        return project
    return None