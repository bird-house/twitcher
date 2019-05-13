from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .token import AccessToken  # flake8: noqa
from .service import Service  # flake8: noqa

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def add_tm_session(request):
    """ Request method that returns a SQLAlchemy session for a request.

    The SQLAlchemy session is managed by a Zope transaction, unless the request has been generated from a
    webtest.TestApp instance for functional testing. In this case:

    - Inspect request.environ dictionary for the SQLAlchemy session referenced by key db.session. Remove the
        session from the request's environment dictionary and return the session.
    - Use the session factory to generate and return a new SQLAlchemy session if there is no entry for db.session
        in the request environment dictionary.

    The webtest.TestApp instance should configure the environment dictionary as follows:
        `testapp = webtest.TestApp(app, extra_environ={'db.session': session, 'tm.active': True})`

    Setting tm.active to True causes the pyramid_tm tween to bypass generating a transaction for the SQLAlchemy
    session on the request.

    This code is taken from:
    https://groups.google.com/forum/#!topic/pylons-discuss/BZCeM_yejEE

    :param request: Pyramid Request instance
    :return: SQLAlchemy session.
    """
    if 'paste.testing' in request.environ and request.environ['paste.testing'] is True:
        if 'db.session' in request.environ:  # and 'db.tm' in request.environ:
            dbsession = request.environ['db.session']
            del request.environ['db.session']
            return dbsession
    session = get_tm_session(request.registry['dbsession_factory'], request.tm)
    return session


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('twitcher.models')``.

    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        # lambda r: get_tm_session(session_factory, r.tm),
        add_tm_session,
        'dbsession',
        reify=True
    )
