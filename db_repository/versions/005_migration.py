from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
purchase = Table('purchase', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('price', Numeric(precision=2)),
    Column('store', String),
    Column('wine', Integer),
)

wine = Table('wine', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
    Column('variety', String),
    Column('year', Integer),
    Column('country', String),
    Column('date_entered', DateTime),
    Column('entered_by', Integer),
    Column('price', Numeric),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['purchase'].create()
    pre_meta.tables['wine'].columns['price'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['purchase'].drop()
    pre_meta.tables['wine'].columns['price'].create()
