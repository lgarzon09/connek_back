from typing                     import List

from sqlalchemy.orm             import Session
from sqlalchemy                 import update, delete, asc

from fastapi                    import Depends, APIRouter, HTTPException, Response
from http                       import HTTPStatus
from provisioning.connection_db import get_db

from provisioning.users_db      import Users
from models.users_models        import UsersInput, UsersResponse

router = APIRouter()

@router.get('/users/find_all/', response_model=List[UsersResponse])
async def find_all_users(db: Session = Depends(get_db)):
    users_in_db = db.query(Users).\
                    order_by(asc(Users.name)).\
                    all()
    if users_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return users_in_db
    

@router.get('/users/find_one/{personal_id}', response_model=UsersResponse)
async def find_one_user(id: int, db: Session = Depends(get_db)):
    user_in_db = db.query(Users).get(id)
    if user_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="User does not exist.")
    return user_in_db


@router.get('/users/find_by_email/{email}', response_model=UsersResponse)
async def find_by_email(email: str, db: Session = Depends(get_db)):
    user_in_db = db.query(Users).\
                    filter(Users.email == email).\
                    first()
    if user_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="Email user does not exist.")
    return user_in_db


@router.post('/users/insert/', response_model=UsersResponse)
async def insert_user(user_in: UsersInput, db: Session = Depends(get_db)):
    user       = Users(**user_in.dict())
    user_in_db = db.query(Users).get(user.id)
    if user_in_db != None:
        raise HTTPException(status_code=409, 
                            detail="The user is yet in the database.")
    db.add( user )
    db.commit()
    db.refresh( user )
    return user

