from fastapi import FastAPI, Body, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..schemas import job_application as jobSchema 
from ..database import get_db
from ..core import oauth2
from ..models import job_application as jobModel

router = APIRouter(
    prefix='/job',
    tags=['Job Applications']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=jobSchema.jobOut)
def createJob(job : jobSchema.createJob , db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    newjob = jobModel.job_application(**job.model_dump(exclude_none=True),
                                      user_id = current_user.id)
    db.add(newjob)
    db.commit()
    db.refresh(newjob)

    return newjob

@router.get('/',status_code=status.HTTP_200_OK,response_model=list[jobSchema.jobOut])
def read(db : Session = Depends(get_db) , current_user = Depends(oauth2.get_current_user)):
    jobs = db.query(jobModel.job_application).filter(jobModel.job_application.user_id == current_user.id).all()
    return jobs

@router.get('/{job_id}',status_code=status.HTTP_200_OK,response_model=jobSchema.jobOut)
def jobId(job_id : int , db : Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
     job = db.query(jobModel.job_application).filter(
          jobModel.job_application.id == job_id,
     ).first()

     if job is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Job not found")
    
     if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this job"
        )
     
     return job

@router.patch('/{job_id}',status_code=status.HTTP_200_OK,response_model=jobSchema.jobOut)
def update(
    job_id: int,
    updated_job: jobSchema.UpdateJob,
    db : Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
    ):
        job =(
             db.query(jobModel.job_application)
             .filter(
                  jobModel.job_application.id == job_id,
                  
        )).first()
        if job is None:
             raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Job was not found"
             )
        if job.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to Update this job"
            )
        updated_data = updated_job.model_dump(exclude_none=True)
        
        for key,value in updated_data.items():
            setattr(job,key,value)

        db.commit()
        db.refresh(job)

        return 

@router.delete('/{job_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(job_id : int,db : Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    job = db.query(jobModel.job_application).filter(
        jobModel.job_application.id == job_id
    ).first()
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Job not found")
    
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this job"
        )
    
    db.delete(job)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

