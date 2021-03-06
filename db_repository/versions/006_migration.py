from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
purchase = Table('purchase', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('price', Numeric),
    Column('store', String),
    Column('wine', Integer),
)

purchase = Table('purchase', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('price', Numeric(precision=2)),
    Column('store', String),
    Column('wine_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['purchase'].columns['wine'].drop()
    post_meta.tables['purchase'].columns['wine_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['purchase'].columns['wine'].create()
    post_meta.tables['purchase'].columns['wine_id'].drop()
