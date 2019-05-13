from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    name = Column(Text)
    type = Column(Text)
    purl = Column(Text)
    public = Column(Integer)  # sqlite does not support Boolean
    verify = Column(Integer)  # sqlite does not support Boolean
    auth = Column(Text)


Index('name_index', Service.name, unique=True, mysql_length=255)
