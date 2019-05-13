from twitcher.namesgenerator import get_random_name


def test_get_random_name():
    name = get_random_name()
    assert len(name) > 3
    assert '_' in name


def test_get_random_name_retry():
    name = get_random_name(retry=True)
    assert len(name) > 3
    assert int(name[-1]) >= 0
