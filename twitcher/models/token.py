from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class AccessToken(Base):
    __tablename__ = 'access_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(Text)
    expires_at = Column(Integer)


Index('token_index', AccessToken.token, unique=True, mysql_length=255)
