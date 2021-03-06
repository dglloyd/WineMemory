from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wine = Table('wine', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50), nullable=False),
    Column('variety', String(length=50)),
    Column('year', Integer),
    Column('country', String(length=50)),
    Column('date_entered', DateTime),
    Column('entered_by', Integer),
    Column('description', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wine'].columns['description'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wine'].columns['description'].drop()
