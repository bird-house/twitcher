from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Union

from .meta import Base


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    name = Column(String(40), unique=True, index=True, nullable=False)
    type = Column(String(40))
    purl = Column(String(255))
    _verify = Column(Integer)  # sqlite does not support Boolean
    auth = Column(String(40))

    @hybrid_property
    def verify(self):
        if self._verify == 1:
            return True
        return False

    @verify.setter
    def verify(self, verify: Union[bool, int]):
        self._verify = int(verify)

    @property
    def public(self):
        """Return true if public access."""
        return self.auth not in ['token', 'cert']

    def json(self):
        return {
            'url': self.url,
            'name': self.name,
            'type': self.type,
            'purl': self.purl,
            'auth': self.auth,
            'public': self.public,
            'verify': self.verify}
