from typing                            import List
     
from sqlalchemy.orm                    import Session
from sqlalchemy                        import delete, asc
     
from fastapi                           import Depends, APIRouter, HTTPException, Response
from http                              import HTTPStatus
from provisioning.connection_db        import get_db

from provisioning.members_db         import Members
from models.members_models           import MembersInput, MembersResponse
from provisioning.users_db             import Users
from provisioning.projects_db             import Projects
                                  
router = APIRouter()


@router.get('/members/find_all/', response_model=List[MembersResponse])
async def find_all_members(db: Session = Depends(get_db)):
    members_in_db = db.query(Members.id.label("id"),
                            Users.id.label("user_id"),
                            Users.photo_url.label("user_photo"),
                            Projects.id.label("project_id"),
                        ).\
                        join(Users, Users.id == Members.user_id).\
                        join(Projects, Projects.id == Members.project_id).\
                        order_by(asc(Users.name)).\
                        all()
    if members_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return members_in_db
    

@router.get('/members/find_one/{id}', response_model=MembersResponse)
async def find_one_member(id: int, db: Session = Depends(get_db)):
    members_in_db = db.query(Members.id.label("id"),
                            Users.id.label("user_id"),
                            Users.photo_url.label("user_photo"),
                            Projects.id.label("project_id"),
                        ).\
                        join(Users, Users.id == Members.user_id).\
                        filter(Members.id == id).\
                        first()
    if members_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="Members does not exist.")
    return members_in_db



@router.post('/members/insert/', response_model=MembersResponse)
async def insert_member(member_in: MembersInput, db: Session = Depends(get_db)):
    member = Members(**member_in.dict())
    db.add( member )
    db.commit()
    db.refresh( member )
    user_in_db        = db.query(Users).get(member.user_id)
    member.user_photo = user_in_db.photo_url
    return member


@router.delete('/members/delete/{id}')
async def delete_member(id: int, db: Session = Depends(get_db)):
    member_in_db = db.query(Members).get(id)
    if member_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="The member id does not exist in database.")
    query = delete(Members).where(Members.id == id).execution_options(synchronize_session="fetch")
    db.execute( query )
    db.commit()
    return "Successful member delete."