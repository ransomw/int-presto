import sqlalchemy as sa
import sqlalchemy.orm as sao

from .base import Base

# https://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship
item_mods = sa.Table(
    'item_mods', Base.metadata,
    sa.Column('item_id', sa.Integer, sa.ForeignKey('item.id'),
              primary_key=True,
    ),
    sa.Column('mod_id', sa.Integer, sa.ForeignKey('item.id'),
              primary_key=True,
    ),
)

class Item(Base):
    __tablename__ = 'item'
    id = sa.Column(sa.Integer,
                   primary_key=True,
    )
    name = sa.Column(sa.String(128),
                     nullable=False,
    )
    restaurant_id = sa.Column(sa.Integer,
                              sa.ForeignKey('restaurant.id'),
                              nullable=False,
    )

    restaurant = sao.relationship('Restaurant',
                                  back_populates='items',
    )

    mods = sao.relationship('Item',
                            secondary=item_mods,
                            primaryjoin=id==item_mods.c.item_id,
                            secondaryjoin=id==item_mods.c.mod_id,
                            cascade='save-update',
    )
