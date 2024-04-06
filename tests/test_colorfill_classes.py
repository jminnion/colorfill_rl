import pytest

import colorfill_gym_env.envs.colorfill as cf

def test_Color_class_getitem_normal():
    color_obj = cf.Color["Blue"]
    assert color_obj.color_index == cf.Color._COLOR_DICT_NAME_TO_INDEX["Blue"]

def test_Color_class_getitem_failing():
    with pytest.raises(IndexError):
        color_obj = cf.Color["Spam"]

# TODO - write tests
