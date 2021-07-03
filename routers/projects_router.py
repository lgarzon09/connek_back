from typing                       import List
  
from sqlalchemy.orm               import Session
from sqlalchemy                   import delete, desc, asc
  
from fastapi                      import Depends, APIRouter, HTTPException, Response
from http                         import HTTPStatus
from provisioning.connection_db   import get_db
  
from provisioning.projects_db         import Projects
from models.projects_models           import ProjectsInput, ProjectsResponse

from provisioning.people_db        import People

router = APIRouter()


@router.get('/projects/find_all/', response_model=List[ProjectsResponse])
async def find_all_projects(db: Session = Depends(get_db)):
    projects_in_db = db.query(\
                            Projects.id.label("id"),
                            Projects.title.label("title"),
                            Projects.message.label("message"),
                            Projects.publish_date.label("publish_date"),
                            Projects.close_date.label("close_date"),
                            Projects.photo_url.label("photo_url"),
                            People.id.label("people_id"),
                        ).\
                        join(People, People.id == Projects.people_id).\
                        all()
    if projects_in_db == []:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)
    return projects_in_db
    

@router.get('/projects/find_one/{id}', response_model=ProjectsResponse)
async def find_one_projects(id: int, db: Session = Depends(get_db)):
    projects_in_db = db.query(\
                            Projects.id.label("id"),
                            Projects.title.label("title"),
                            Projects.message.label("message"),
                            Projects.publish_date.label("publish_date"),
                            Projects.close_date.label("close_date"),
                            Projects.photo_url.label("photo_url"),
                            People.id.label("people_id"),
                        ).\
                        join(People, People.id == Projects.people_id).\
                        filter(Projects.id == id).\
                        first()
    if projects_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="Projects does not exist.")
    return projects_in_db


@router.post('/projects/insert/', response_model=ProjectsResponse)
async def insert_projects(projects_in: ProjectsInput, db: Session = Depends(get_db)):
    projects       = Projects(**projects_in.dict())
    projects_in_db = db.query(Projects).\
                    filter(Projects.title == projects.title).\
                    first()
    if projects_in_db != None:
        raise HTTPException(status_code=409, 
                            detail="The projects is yet in the database.")
    db.add( projects )
    db.commit()
    db.refresh( projects )
    return projects


@router.put('/projects/update/')
async def update_projects(db: Session = Depends(get_db)):
    #TODO define what to update
    return None


@router.delete('/projects/delete/{id}')
async def delete_projects(id: int, db: Session = Depends(get_db)):
    projects_in_db = db.query(Projects).get(id)
    if projects_in_db == None:
        raise HTTPException(status_code=404, 
                            detail="The projects id does not exist in database.")
    query = delete(Projects).\
            where(Projects.id == id).\
            execution_options(synchronize_session="fetch")
    db.execute( query )
    db.commit()
    return "Successful delete."