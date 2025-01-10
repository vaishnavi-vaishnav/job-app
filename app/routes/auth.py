from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, User
from app.models.user import UserCreate, User,UserType
from app.utils.auth_utils import get_password_hash, verify_password, create_access_token
from bson import ObjectId

router = APIRouter()

@router.post("/signup")
async def signup(request: Request, user: UserCreate):
    # Check if user exists
    if await request.app.mongodb["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate user type
    if user.user_type not in [UserType.CANDIDATE, UserType.RECRUITER]:
        raise HTTPException(status_code=400, detail="Invalid user type. Must be either 'candidate' or 'recruiter'")
    
    # Create new user
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["_id"] = str(ObjectId())
    
    await request.app.mongodb["users"].insert_one(user_dict)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await request.app.mongodb["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Include user type in token
    access_token = create_access_token(data={
        "sub": str(user["_id"]),
        "user_type": user["user_type"]
    })
    return {"access_token": access_token, "token_type": "bearer"}