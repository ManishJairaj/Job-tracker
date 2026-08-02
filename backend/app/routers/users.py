from ..core import security
from ..schemas import user as userSchema
from ..models import user as userModel
from ..database import get_db
from fastapi import FastAPI, Body, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= '/users',
    tags= ['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=userSchema.UserResponse)
def create( user : userSchema.UserCreate , db : Session = Depends(get_db)):

    formattedEmail = user.email.strip().lower()
    check_user = (db.query(userModel.User)
                  .filter(userModel.User.email == formattedEmail)
                  .first()
                )
    
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email is already registered")
    
    user_data = user.model_dump(exclude={"password","email"})
    hashed_password = security.hash(user.password)

    new_user = userModel.User(  **user_data,
                                email=formattedEmail,
                                password=hashed_password
                            )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",status_code=status.HTTP_200_OK,response_model= list[userSchema.UserResponse])
def read( db : Session = Depends(get_db)):
    posts = db.query(userModel.User).all()
    return posts

