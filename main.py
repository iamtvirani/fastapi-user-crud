from fastapi import FastAPI, HTTPException
from app.models import User, UserCreate, UserUpdate
from app.database import users_db

app = FastAPI()

current_id = 0   # auto increment counter


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


# Get all users
@app.get("/users")
def get_users():
    return users_db


# Create user
@app.post("/users")
def create_user(user: UserCreate):
    global current_id

    for existing_user in users_db:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    current_id += 1

    new_user = User(
        id=current_id,
        name=user.name,
        email=user.email
    )

    users_db.append(new_user)
    return new_user

# Get single user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


# Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return {"message": "User deleted"}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_data: UserUpdate):

    for user in users_db:

        if user.id == user_id:

            # 🔴 check duplicate email if email is changing
            if updated_data.email:
                for existing_user in users_db:
                    if existing_user.email == updated_data.email and existing_user.id != user_id:
                        raise HTTPException(
                            status_code=400,
                            detail="Email already registered"
                        )

            # 🟢 Update fields if provided
            if updated_data.name:
                user.name = updated_data.name

            if updated_data.email:
                user.email = updated_data.email

            return user

    raise HTTPException(status_code=404, detail="User not found")