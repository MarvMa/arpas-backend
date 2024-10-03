from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import Instance, Project, Item, get_db
from app.schemas import InstanceCreate, InstanceRead

router = APIRouter()


@router.post("/instances/", response_model=InstanceRead)
def create_instance(instance: InstanceCreate, db: Session = Depends(get_db)):
    """
       Create a new instance.

       This endpoint allows the creation of a new instance associated with a project and an item.
       The instance includes transformations like position, rotation, and scale.

       Parameters:
           - instance: JSON body containing the project_id, item_id, and transformation details.
           - db: Database session (injected).

       Returns:
           - The newly created instance, including its ID and associated project/item details.

       Raises:
           - 404 HTTPException if the project or item is not found.
       """
    # Ensure the project and item exist
    project = db.query(Project).filter(Project.id == instance.project_id).first()
    item = db.query(Item).filter(Item.id == instance.item_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Create and save the new instance
    new_instance = Instance(
        project_id=instance.project_id,
        item_id=instance.item_id,
        position_x=instance.position_x,
        position_y=instance.position_y,
        position_z=instance.position_z,
        rotation_x=instance.rotation_x,
        rotation_y=instance.rotation_y,
        rotation_z=instance.rotation_z,
        scale_x=instance.scale_x,
        scale_y=instance.scale_y,
        scale_z=instance.scale_z
    )
    db.add(new_instance)
    db.commit()
    db.refresh(new_instance)
    return new_instance


@router.put("/instances/{instance_id}", response_model=InstanceRead)
def update_instance(instance_id: int, instance_update: InstanceCreate, db: Session = Depends(get_db)):
    """
       Update an existing instance.

       This endpoint allows updating an existing instance's transformation details (position, rotation, and scale),
       as well as changing the associated project or item.

       Parameters:
           - instance_id: The unique ID of the instance to update.
           - instance_update: JSON body containing the updated project_id, item_id, and transformation details.
           - db: Database session (injected).

       Returns:
           - The updated instance, including its new details.

       Raises:
           - 404 HTTPException if the instance, project, or item is not found.
    """
    # Ensure the instance exists
    existing_instance = db.query(Instance).filter(Instance.id == instance_id).first()
    if existing_instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")

    # Ensure the project and item exist
    project = db.query(Project).filter(Project.id == instance_update.project_id).first()
    item = db.query(Item).filter(Item.id == instance_update.item_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the instance's attributes
    existing_instance.project_id = instance_update.project_id
    existing_instance.item_id = instance_update.item_id
    existing_instance.position_x = instance_update.position_x
    existing_instance.position_y = instance_update.position_y
    existing_instance.position_z = instance_update.position_z
    existing_instance.rotation_x = instance_update.rotation_x
    existing_instance.rotation_y = instance_update.rotation_y
    existing_instance.rotation_z = instance_update.rotation_z
    existing_instance.scale_x = instance_update.scale_x
    existing_instance.scale_y = instance_update.scale_y
    existing_instance.scale_z = instance_update.scale_z

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_instance)
    return existing_instance


@router.get("/instances/{instance_id}", response_model=InstanceRead)
def get_instance(instance_id: int, db: Session = Depends(get_db)):
    """
       Retrieve an instance by its ID.

       This endpoint retrieves an instance's details using its unique ID.
       If the instance is not found, a 404 error is returned.

       Parameters:
           - instance_id: The unique ID of the instance to retrieve.
           - db: Database session (injected).

       Returns:
           - The instance's details, including its transformations and associated project/item.

       Raises:
           - 404 HTTPException if the instance is not found.
       """
    instance = db.query(Instance).filter(Instance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance


@router.get("/instances/", response_model=List[InstanceRead])
def list_instances(db: Session = Depends(get_db)):
    """
        List all instances.

        This endpoint retrieves and returns all instances stored in the database.

        Parameters:
            - db: Database session (injected).

        Returns:
            - A list of instances, each containing its transformations and associated project/item.
        """
    instances = db.query(Instance).all()
    return instances


@router.delete("/instances/{instance_id}", status_code=204)
def delete_instance(instance_id: int, db: Session = Depends(get_db)):
    """
        Delete an instance by its ID.

        This endpoint deletes an instance using its unique ID.
        If the instance is not found, a 404 error is returned.

        Parameters:
            - instance_id: The unique ID of the instance to delete.
            - db: Database session (injected).

        Returns:
            - A message confirming that the instance has been deleted successfully.

        Raises:
            - 404 HTTPException if the instance is not found.
        """
    instance = db.query(Instance).filter(Instance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")
    db.delete(instance)
    db.commit()
    return {"message": "Instance deleted successfully"}
