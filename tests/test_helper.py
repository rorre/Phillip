from phillip.helper import has_user


def test_empty_target():
    assert not has_user({"id": 0}, [])


def test_find_user():
    assert has_user({"id": 1}, [{"id": 8}, {"id": 1}])


def test_no_user():
    assert not has_user({"id": 99}, [{"id": 1}])
