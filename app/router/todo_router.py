from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app import model
from app.schemas import todo_schema

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=todo_schema.TodoResponse)
async def create_todo(todo: todo_schema.TodoCreate, db: Session = Depends(get_db)):
    current_time = datetime.now(timezone.utc)

    new_todo = model.Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        created_at=current_time,
        updated_at=current_time,
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/", response_model=list[todo_schema.TodoResponse])
async def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(model.Todo).all()
    return todos


@router.get("/{todo_id}", response_model=todo_schema.TodoResponse)
async def get_one_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=todo_schema.TodoResponse)
async def update_todo(todo_id: int, todo_update: todo_schema.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.due_date is not None:
        todo.due_date = todo_update.due_date

    # Always update the timestamp
    todo.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": f"Todo with id {todo_id} deleted successfully"}
