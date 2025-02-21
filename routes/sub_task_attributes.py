from fastapi import APIRouter, HTTPException
from models import SubTaskAttribute, SubTaskAttributeCreate, SubTaskAttributeUpdate
import crud

router = APIRouter(prefix="/sub_task_attributes", tags=["Sub Task Attributes"])

@router.post("/", response_model=SubTaskAttribute)
def create_sub_task_attribute_endpoint(attribute: SubTaskAttributeCreate):
    crud.create_sub_task_attribute(attribute.sub_task_id, attribute.user_id, attribute.attribute_key, attribute.attribute_value)
    created_attribute = crud.get_last_inserted_sub_task_attribute()  # Implement this helper if desired.
    if not created_attribute:
        raise HTTPException(status_code=404, detail="Sub Task Attribute not created")
    return created_attribute

@router.get("/{attribute_id}", response_model=SubTaskAttribute)
def get_sub_task_attribute(attribute_id: int):
    attribute = crud.get_sub_task_attribute_by_id(attribute_id)
    if not attribute:
        raise HTTPException(status_code=404, detail="Sub Task Attribute not found")
    return attribute

@router.put("/{attribute_id}", response_model=SubTaskAttribute)
def update_sub_task_attribute_endpoint(attribute_id: int, attribute_update: SubTaskAttributeUpdate):
    crud.update_sub_task_attribute(attribute_id, attribute_update.attribute_key, attribute_update.attribute_value)
    updated_attribute = crud.get_sub_task_attribute_by_id(attribute_id)
    if not updated_attribute:
        raise HTTPException(status_code=404, detail="Sub Task Attribute not found")
    return updated_attribute

@router.delete("/{attribute_id}")
def delete_sub_task_attribute_endpoint(attribute_id: int):
    crud.delete_sub_task_attribute(attribute_id)
    return {"detail": "Sub Task Attribute deleted"}
