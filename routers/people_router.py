from typing                            import List
        
from sqlalchemy.orm                    import Session
from sqlalchemy                        import update, delete, and_, asc
        
from fastapi                           import Depends, APIRouter, HTTPException, Response
from http                              import HTTPStatus
from provisioning.connection_db        import get_db

from provisioning.people_db         import People
from models.people_models           import PeopleInput, PeopleResponse
from provisioning.users_db             import Users

router = APIRouter()


@router.get('/people/find_all/', response_model=List[PeopleResponse])
async def find_all_people(db: Session = Depends(get_db)):
    people_in_db = db.query(
                            People.id.label("id"),
                            People.country.label("country"),
                            People.city.label("city"),
                            People.sector.label("sector"),
                            People.about.label("about"),
                            People.phone.label("phone"),
                            People.birthday.label("birthday"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == People.user_id).\
                        order_by(asc(Users.name)).\
                        all()
    if people_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return people_in_db
    

@router.get('/people/find_one/{id}', response_model=PeopleResponse)
async def find_one_people(id: int, db: Session = Depends(get_db)):
    people_in_db = db.query(
                            People.id.label("id"),
                            People.country.label("country"),
                            People.city.label("city"),
                            People.sector.label("sector"),
                            People.about.label("about"),
                            People.phone.label("phone"),
                            People.birthday.label("birthday"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == People.user_id).\
                        filter(People.id == id).\
                        first()
    if people_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="People does not exist.")
    return people_in_db


@router.get('/people/find_by_user/{user_id}', response_model=List[PeopleResponse])
async def find_people_by_user(user_id: int, db: Session = Depends(get_db)):
    people_in_db = db.query(
                            People.id.label("id"),
                            People.country.label("country"),
                            People.city.label("city"),
                            People.sector.label("sector"),
                            People.about.label("about"),
                            People.phone.label("phone"),
                            People.birthday.label("birthday"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == People.user_id).\
                        filter(People.user_id == user_id).\
                        order_by(asc(Users.name)).\
                        all()
    if people_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return people_in_db


@router.post('/people/insert/', response_model=PeopleResponse)
async def insert_people(people_in: PeopleInput, db: Session = Depends(get_db)):
    people       = People(**people_in.dict())
    people_in_db = db.query(People).\
                    filter(People.user_id == people.user_id).\
                    first()
    if people_in_db != None:
        raise HTTPException(status_code=409, 
                            detail="The people is yet in the database.")
    db.add( people )
    db.commit()
    db.refresh( people )
    user_in_db                     = db.query(Users).get(people.user_id)
    people.user_name             = user_in_db.name
    people.user_email            = user_in_db.email
    people.user_photo            = user_in_db.photo_url
    return people


@router.delete('/people/delete/{id}')
async def delete_people(id: int, db: Session = Depends(get_db)):
    people_in_db = db.query(People).get(id)
    if people_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="The people id does not exist in database.")
    query = delete(People).\
            where(People.id == id).\
            execution_options(synchronize_session="fetch")
    db.execute( query )
    db.commit()
    return "Successful delete."