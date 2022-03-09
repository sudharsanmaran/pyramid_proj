import uuid

from sqlalchemy import (
    Column,Integer,Text, String,ForeignKey
)
from sqlalchemy.orm import relationship

from .meta import Base


class UserModel(Base):
    __tablename__ = 'UserModel'
    id = Column(String, primary_key=True , default=lambda : str(uuid.uuid4()), index=True)
    name = Column(String, index=True)
    email = Column(Text,unique=True, index=True,nullable=False)
    password=Column(Text)

    def __repr__(self):
        return self.name
    #1 to 1
    # no back_populates due to multiple foriegn keys
    # details=relationship("UserDetails", back_populates="user")
    # team_member = relationship("UserDetails", back_populates="user_incharge")

class UserDetails(Base):
    __tablename__="UserDetails"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    emp_code=Column(Integer,index=True)
    phone_no=Column(Integer)
    user_id=Column(String, ForeignKey("UserModel.id"))
    user_incharge_id=Column(String, ForeignKey("UserModel.id"))

    #1 to 1
    user=relationship("UserModel",foreign_keys=[user_id])
    user_incharge = relationship("UserModel", foreign_keys=[user_incharge_id] )
