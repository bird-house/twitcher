from twitcher.adapter import import_adapter, get_adapter_factory, TWITCHER_ADAPTER_DEFAULT
from twitcher.adapter.base import AdapterInterface
from twitcher.adapter.default import DefaultAdapter
from twitcher.interface import OWSSecurityInterface

from pyramid.testing import DummyRequest
from pathlib import Path
import pytest
import shutil
import site
import os


def test_import_adapter():
    adapter = import_adapter('twitcher.adapter.default.DefaultAdapter')
    assert adapter is DefaultAdapter, "Expect {!s}, but got {!s}".format(DefaultAdapter, adapter)
    assert isinstance(adapter({}), AdapterInterface), \
        "Expect {!s}, but got {!s}".format(AdapterInterface, type(adapter))


def test_adapter_factory_default_explicit():
    settings = {'twitcher.adapter': TWITCHER_ADAPTER_DEFAULT}
    adapter = get_adapter_factory(settings)
    assert isinstance(adapter, DefaultAdapter), "Expect {!s}, but got {!s}".format(DefaultAdapter, type(adapter))


def test_adapter_factory_none_specified():
    adapter = get_adapter_factory({})
    assert isinstance(adapter, DefaultAdapter), "Expect {!s}, but got {!s}".format(DefaultAdapter, type(adapter))


# noinspection PyAbstractClass,PyMethodMayBeStatic
class DummyAdapter(AdapterInterface):
    def owssecurity_factory(self):
        class DummyOWSSecurity(OWSSecurityInterface):
            def verify_request(self, request): return True   # noqa: E704
        return DummyOWSSecurity()


# noinspection PyPep8Naming
def test_adapter_factory_DummyAdapter_valid_import_with_init():
    settings = {'twitcher.adapter': DummyAdapter({}).name}
    adapter = get_adapter_factory(settings)
    assert isinstance(adapter, DummyAdapter), "Expect {!s}, but got {!s}".format(DummyAdapter, type(adapter))


def make_path(base, other='__init__.py'):
    return str(Path(base) / Path(other))


def test_adapter_factory_TmpAdapter_valid_import_installed_without_init():
    """
    Test a valid installed adapter import by setting although not located under same directory,
    with much deeper structure, and without any '__init__.py' defining a python 'package'.
    """

    mod_pkg = 'test_package'
    mod_base = site.getsitepackages()[0]
    try:
        mod_name = '{}.module.submodule.section'.format(mod_pkg)
        mod_path = make_path(mod_base, mod_name.replace('.', '/'))
        mod_file_name = 'file'
        mod_file = make_path(mod_path, '{}.py'.format(mod_file_name))
        mod_class = 'TmpAdapter'
        os.makedirs(mod_path, exist_ok=True)
        with open(mod_file, 'w') as f:
            f.writelines([
                "from twitcher.adapter.base import AdapterInterface\n\n",
                "class {}(AdapterInterface):\n".format(mod_class),
                "    pass\n"
            ])
        mod_import = '.'.join([mod_name, mod_file_name, mod_class])

        settings = {'twitcher.adapter': mod_import}
        adapter = get_adapter_factory(settings)
        adapter_mod_name = '.'.join([adapter.__module__, type(adapter).__name__])
        assert not isinstance(adapter, DefaultAdapter)
        assert isinstance(adapter, AdapterInterface)
        assert adapter_mod_name == mod_import
    finally:
        shutil.rmtree(make_path(mod_base, mod_pkg), ignore_errors=True)


# noinspection PyAbstractClass
class DummyAdapterFake(object):
    pass


# noinspection PyPep8Naming
def test_adapter_factory_TestAdapter_invalid_raised():
    # fake adapter doesn't have 'name' property, provide at least same functionality
    dummy_name = '{}.{}'.format(DummyAdapterFake.__module__, DummyAdapterFake.__name__)
    settings = {'twitcher.adapter': dummy_name}
    with pytest.raises(TypeError) as err:
        get_adapter_factory(settings)
        pytest.fail(msg="Invalid adapter not inheriting from 'AdapterInterface' should raise on import.")
    adapter_str = '{}.{}'.format(AdapterInterface.__module__, AdapterInterface.__name__)
    assert adapter_str in str(err.value), "Expected to have full adapter import string in error message."


# noinspection PyTypeChecker
def test_adapter_factory_call_owssecurity_factory():
    settings = {'twitcher.adapter': DummyAdapter({}).name}
    adapter = get_adapter_factory(settings)
    security = adapter.owssecurity_factory()
    assert isinstance(security, OWSSecurityInterface)
    assert security.verify_request(DummyRequest()) is True, "Requested adapter should have been called."
