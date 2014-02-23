from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wine_rating = Table('wine_rating', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('rating', Integer, default=ColumnDefault(0)),
    Column('user_id', Integer),
    Column('wine_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wine_rating'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wine_rating'].columns['user_id'].drop()
