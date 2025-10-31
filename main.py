from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from database import Base, engine, get_db
from models import User, Task
from schemas import UserCreate, UserOut, TaskCreate, TaskUpdate, TaskOut
from crud import create_user, get_user, create_task, get_tasks, get_task, update_task, delete_task, get_user_by_email
from auth import create_access_token, verify_token, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ---------- Auth ----------
@app.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user.username, user.email, user.password)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ---------- Task ----------
@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_task(db, task, current_user.id)

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(status: str = Query(None), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_tasks(db, current_user.id, status)

@app.put("/tasks/{task_id}", response_model=TaskOut)
def edit_task(task_id: int, task: TaskUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return update_task(db, task_id, task)

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    delete_task(db, task_id)
    return {"detail": "Task deleted successfully"}
