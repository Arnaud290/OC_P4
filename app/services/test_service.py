"""alpha and numeric test service module"""
from ..views.view import View


class TestService:
    """Class for all tests user input"""
    result = None

    @classmethod
    def test_alpha(cls, test_element=None, title=None, test_loop=True):
        """ test for alpha inputs"""
        while True:
            if title:
                test = View.request(title).capitalize()
            else:
                test = View.get_choice().capitalize()
            if test == '' and test_loop is False:
                return None
            if test == '' and test_loop:
                continue
            if test_element:
                if test in test_element:
                    return test
                    pass
                else:
                    continue
            else:
                return test

    @classmethod
    def test_num(
                    cls,
                    title=None,
                    test_element=None,
                    test_not_element=None,
                    test_range_element=None,
                    test_loop=True,
                    even_test=False,
                    positif_num=False,
                    modif_num=None
                ):
        """test for numeric inputs"""
        while True:
            if title is not None:
                test = View.request(title)
            else:
                test = View.get_choice
            if test == '' and not test_loop:
                return None
            try:
                test = abs(int(test))
            except ValueError:
                continue
            else:
                if modif_num:
                    test += modif_num
                if test_element is not None:
                    if test in test_element:
                        pass
                    else:
                        continue
                if test_not_element is not None:
                    if test not in test_not_element:
                        pass
                    else:
                        continue
                if test_range_element is not None:
                    if test not in range(test_range_element):
                        continue
                    else:
                        pass
                if even_test:
                    if test % 2 != 0:
                        View.indication('the number must be an even number')
                        View.pause()
                        continue
                    else:
                        pass
                if positif_num:
                    if test <= 0:
                        View.indication('the number must be positif')
                        View.pause()
                        continue
                    else:
                        pass
                return test
