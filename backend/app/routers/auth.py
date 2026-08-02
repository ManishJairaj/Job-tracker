from fastapi import Depends,APIRouter,Response,status ,HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,utils
from ..schemas import token as tokenSchema
from ..core import oauth2,security
from ..models import user as userModel

router = APIRouter(
    tags= ["Authentication"]
)

@router.post("/login",response_model=tokenSchema.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
    user = db.query(userModel.User).filter(userModel.User.email == user_credentials.username).first()
    # username =
    # password =
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    if not security.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data={'user_id' : user.id})
    return {
        'access_token' : access_token,
        'token_type' : "bearer"
    }
