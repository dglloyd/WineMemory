from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
purchase = Table('purchase', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('price', Numeric(precision=2)),
    Column('store', String),
    Column('wine_id', Integer),
    Column('drank', Boolean),
    Column('user_id', Integer),
    Column('date_entered', DateTime),
)

wine_rating = Table('wine_rating', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('rating', Integer, default=ColumnDefault(0)),
    Column('notes', Text),
    Column('user_id', Integer),
    Column('wine_id', Integer),
    Column('date_entered', DateTime),
)

wine = Table('wine', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String, nullable=False),
    Column('variety', String),
    Column('year', Integer),
    Column('country', String),
    Column('date_entered', DateTime),
    Column('entered_by', Integer),
    Column('description', Text),
    Column('notes', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['purchase'].columns['date_entered'].create()
    post_meta.tables['wine_rating'].columns['date_entered'].create()
    post_meta.tables['wine_rating'].columns['notes'].create()
    pre_meta.tables['wine'].columns['notes'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['purchase'].columns['date_entered'].drop()
    post_meta.tables['wine_rating'].columns['date_entered'].drop()
    post_meta.tables['wine_rating'].columns['notes'].drop()
    pre_meta.tables['wine'].columns['notes'].create()
