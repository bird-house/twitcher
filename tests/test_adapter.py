from twitcher.adapter import import_adapter, get_adapter_factory, TWITCHER_ADAPTER_DEFAULT
from twitcher.adapter.base import AdapterInterface
from twitcher.adapter.default import DefaultAdapter
import pytest


def test_import_adapter():
    adapter = import_adapter('twitcher.adapter.default.DefaultAdapter')
    assert adapter is DefaultAdapter, "Expect {!s}, but got {!s}".format(DefaultAdapter, adapter)
    assert isinstance(adapter(), AdapterInterface), "Expect {!s}, but got {!s}".format(AdapterInterface, type(adapter))


def test_adapter_factory_default_explicit():
    settings = {'twitcher.adapter': TWITCHER_ADAPTER_DEFAULT}
    adapter = get_adapter_factory(settings)
    assert isinstance(adapter, DefaultAdapter), "Expect {!s}, but got {!s}".format(DefaultAdapter, type(adapter))


def test_adapter_factory_none_specified():
    adapter = get_adapter_factory({})
    assert isinstance(adapter, DefaultAdapter), "Expect {!s}, but got {!s}".format(DefaultAdapter, type(adapter))


# noinspection PyAbstractClass
class TestAdapter(AdapterInterface):
    pass


# noinspection PyPep8Naming
def test_adapter_factory_TestAdapter_valid_import():
    settings = {'twitcher.adapter': '{}.{}'.format(TestAdapter.__module__, TestAdapter.__name__)}
    adapter = get_adapter_factory(settings)
    assert isinstance(adapter, TestAdapter), "Expect {!s}, but got {!s}".format(TestAdapter, type(adapter))


# noinspection PyAbstractClass
class TestAdapterFake(object):
    pass


# noinspection PyPep8Naming
def test_adapter_factory_TestAdapter_invalid_raised():
    settings = {'twitcher.adapter': '{}.{}'.format(TestAdapterFake.__module__, TestAdapterFake.__name__)}
    with pytest.raises(TypeError) as err:
        get_adapter_factory(settings)
        pytest.fail(msg="Invalid adapter not inheriting from 'AdapterInterface' should raise on import.")
    adapter_str = '{}.{}'.format(AdapterInterface.__module__, AdapterInterface.__name__)
    assert adapter_str in str(err), "Expected to have full adapter import string in error message."
