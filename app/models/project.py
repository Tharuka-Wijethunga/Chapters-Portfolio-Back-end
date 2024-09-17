from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional
from bson import ObjectId
from datetime import datetime
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class ProjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)


    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

class ProjectModel(BaseModel):
    id: ProjectId = Field(default_factory=ProjectId, alias="_id")
    name: str
    description: str
    image: str
    visibility: bool = True
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    visibility: Optional[bool] = None
    featured: Optional[bool] = None

class ProjectSearch(BaseModel):
    query: str

# MongoDB Pipelines
def get_projects_pipeline(filter_params=None, sort_params=None, page=1, page_size=10):
    pipeline = []

    if filter_params:
        match_stage = {"$match": {}}
        if "name" in filter_params:
            match_stage["$match"]["name"] = {"$regex": filter_params["name"], "$options": "i"}
        if "visibility" in filter_params:
            match_stage["$match"]["visibility"] = filter_params["visibility"]
        pipeline.append(match_stage)

    if sort_params:
        sort_stage = {"$sort": {sort_params["field"]: 1 if sort_params["direction"] == "ascending" else -1}}
        pipeline.append(sort_stage)

    pipeline.extend([
        {"$skip": (page - 1) * page_size},
        {"$limit": page_size}
    ])

    return pipeline

def search_projects_pipeline(query):
    return [
        {
            "$match": {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ],
                "visibility": True
            }
        }
    ]