from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Date,DateTime,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class job_application(Base):
    __tablename__ = "JobApplication"
    id = Column(Integer,primary_key=True,nullable = False)
    role = Column(String,nullable=False)
    status = Column(String,nullable=False,default="Applied")
    applied_date = Column(Date,nullable=False,server_default=func.current_date())

    company = Column(String,nullable= False)
    job_url = Column(String,nullable=False)
    location = Column(String,nullable = False)
    notes = Column(Text,nullable=True)

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)


