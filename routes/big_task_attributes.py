from fastapi import APIRouter, HTTPException
from models import BigTaskAttribute, BigTaskAttributeCreate, BigTaskAttributeUpdate
import crud

router = APIRouter(prefix="/big_task_attributes", tags=["Big Task Attributes"])

@router.post("/", response_model=BigTaskAttribute)
def create_big_task_attribute_endpoint(attribute: BigTaskAttributeCreate):
    crud.create_big_task_attribute(attribute.big_task_id, attribute.user_id, attribute.attribute_key, attribute.attribute_value)
    created_attribute = crud.get_last_inserted_big_task_attribute()  # Implement this helper if desired.
    if not created_attribute:
        raise HTTPException(status_code=404, detail="Big Task Attribute not created")
    return created_attribute

@router.get("/{attribute_id}", response_model=BigTaskAttribute)
def get_big_task_attribute(attribute_id: int):
    attribute = crud.get_big_task_attribute_by_id(attribute_id)
    if not attribute:
        raise HTTPException(status_code=404, detail="Big Task Attribute not found")
    return attribute

@router.put("/{attribute_id}", response_model=BigTaskAttribute)
def update_big_task_attribute_endpoint(attribute_id: int, attribute_update: BigTaskAttributeUpdate):
    crud.update_big_task_attribute(attribute_id, attribute_update.attribute_key, attribute_update.attribute_value)
    updated_attribute = crud.get_big_task_attribute_by_id(attribute_id)
    if not updated_attribute:
        raise HTTPException(status_code=404, detail="Big Task Attribute not found")
    return updated_attribute

@router.delete("/{attribute_id}")
def delete_big_task_attribute_endpoint(attribute_id: int):
    crud.delete_big_task_attribute(attribute_id)
    return {"detail": "Big Task Attribute deleted"}
