from typing                            import List
        
from sqlalchemy.orm                    import Session
from sqlalchemy                        import update, delete, and_, asc
        
from fastapi                           import Depends, APIRouter, HTTPException, Response
from http                              import HTTPStatus
from provisioning.connection_db        import get_db

from provisioning.companies_db         import Companies
from models.companies_models           import CompaniesInput, CompaniesResponse
from provisioning.users_db             import Users

router = APIRouter()


@router.get('/companies/find_all/', response_model=List[CompaniesResponse])
async def find_all_companies(db: Session = Depends(get_db)):
    companies_in_db = db.query(
                            Companies.id.label("id"),
                            Companies.url.label("url"),
                            Companies.country.label("country"),
                            Companies.city.label("city"),
                            Companies.sector.label("sector"),
                            Companies.company_type.label("company_type"),
                            Companies.description.label("description"),
                            Companies.birthday.label("birthday"),
                            Companies.workers.label("workers"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == Companies.user_id).\
                        order_by(asc(Users.name)).\
                        all()
    if companies_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return companies_in_db
    

@router.get('/companies/find_one/{id}', response_model=CompaniesResponse)
async def find_one_companies(id: int, db: Session = Depends(get_db)):
    companies_in_db = db.query(
                            Companies.id.label("id"),
                            Companies.url.label("url"),
                            Companies.country.label("country"),
                            Companies.city.label("city"),
                            Companies.sector.label("sector"),
                            Companies.company_type.label("company_type"),
                            Companies.description.label("description"),
                            Companies.birthday.label("birthday"),
                            Companies.workers.label("workers"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == Companies.user_id).\
                        filter(Companies.id == id).\
                        first()
    if companies_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="Companies does not exist.")
    return companies_in_db


@router.get('/companies/find_by_user/{user_id}', response_model=List[CompaniesResponse])
async def find_companies_by_user(user_id: int, db: Session = Depends(get_db)):
    companies_in_db = db.query(
                            Companies.id.label("id"),
                            Companies.url.label("url"),
                            Companies.country.label("country"),
                            Companies.city.label("city"),
                            Companies.sector.label("sector"),
                            Companies.company_type.label("company_type"),
                            Companies.description.label("description"),
                            Companies.birthday.label("birthday"),
                            Companies.workers.label("workers"),
                            Users.id.label("user_id"),
                            Users.name.label("user_name"),
                            Users.email.label("user_email"),
                            Users.photo_url.label("user_photo"),
                        ).\
                        join(Users, Users.id == Companies.user_id).\
                        filter(Companies.user_id == user_id).\
                        order_by(asc(Users.name)).\
                        all()
    if companies_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return companies_in_db


@router.post('/companies/insert/', response_model=CompaniesResponse)
async def insert_companies(companies_in: CompaniesInput, db: Session = Depends(get_db)):
    companies       = Companies(**companies_in.dict())
    companies_in_db = db.query(Companies).\
                    filter(Companies.user_id == companies.user_id).\
                    first()
    if companies_in_db != None:
        raise HTTPException(status_code=409, 
                            detail="The companies is yet in the database.")
    db.add( companies )
    db.commit()
    db.refresh( companies )
    user_in_db                     = db.query(Users).get(companies.user_id)
    companies.user_name             = user_in_db.name
    companies.user_email            = user_in_db.email
    companies.user_photo            = user_in_db.photo_url
    return companies


@router.delete('/companies/delete/{id}')
async def delete_companies(id: int, db: Session = Depends(get_db)):
    companies_in_db = db.query(Companies).get(id)
    if companies_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="The companies id does not exist in database.")
    query = delete(Companies).\
            where(Companies.id == id).\
            execution_options(synchronize_session="fetch")
    db.execute( query )
    db.commit()
    return "Successful delete."