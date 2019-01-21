import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = sa.Column(sa.Integer,
                   primary_key=True,
    )
    name = sa.Column(sa.String(128),
                     nullable=False,
    )

    items = sao.relationship('Item',
                             back_populates='restaurant',
                             cascade='save-update',
    )
