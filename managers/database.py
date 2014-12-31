#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager

manager = Manager(usage='Perform database operations')


@manager.command
def create():
    '''Creates the SQLAlchemy databases as configured'''

    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO
    from app import db
    import os.path

    db.create_all()

    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI,
                            SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI,
                            SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))


@manager.command
def downgrade():
    '''Downgrades the SQLAlchemy databases'''

    from migrate.versioning import api
    from config import SQLALCHEMY_DATABASE_URI
    from config import SQLALCHEMY_MIGRATE_REPO

    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v
                  - 1)

    print 'Current database version: ' \
        + str(api.db_version(SQLALCHEMY_DATABASE_URI,
              SQLALCHEMY_MIGRATE_REPO))


@manager.command
def migrate():
    '''Migrates the SQLAlchemy databases for model changes'''

    import imp
    from migrate.versioning import api
    from app import db
    from config import SQLALCHEMY_MIGRATE_REPO
    from config import SQLALCHEMY_DATABASE_URI

    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' \
        % (api.db_version(SQLALCHEMY_DATABASE_URI,
           SQLALCHEMY_MIGRATE_REPO) + 1)

    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI,
                                 SQLALCHEMY_MIGRATE_REPO)

    exec old_model in tmp_module.__dict__

    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    open(migration, 'wt').write(script)

    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    print 'New migration saved as : ' + migration
    print 'Current database version : ' \
        + str(api.db_version(SQLALCHEMY_DATABASE_URI,
              SQLALCHEMY_MIGRATE_REPO))


@manager.command
def upgrade():
    '''Upgrades the SQLAlchemy databases'''

    from migrate.versioning import api
    from config import sqlalchemy_database_uri
    from config import sqlalchemy_migrate_repo

    api.upgrade(sqlalchemy_database_uri, sqlalchemy_migrate_repo)

    print 'current database version: ' \
        + str(api.db_version(sqlalchemy_database_uri,
              sqlalchemy_migrate_repo))

