from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # sqlalchemy relationship need to retrieve data from other table (User)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
