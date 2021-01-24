"""Test service module"""
from ..views.view import View

class TestService:
    """Class for all tests user input"""
    result = None
    @classmethod
    def test_alpha(cls, test_element, title=None, test_loop=True):
        """ test for alpha inputs"""
        while True:
            if title:
                test = View.request(title).upper()
            else:
                test = View.get_choice().upper()
            if not test and not test_loop:
                return None
            if test in test_element:
                return test
            else:
                continue 
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
        """test for nums inputs"""
        while True:
            if title:
                test = View.request(title)
            else:
                 test = View.get_choice
            if not test and not test_loop:
                return None  
            try:
                test = abs(int(test))
            except ValueError:
                continue
            else:
                if modif_num:
                    test += modif_num
                if positif_num:
                    if test <= 0:
                        View.indication('the number must be positif')
                        View.pause()
                        continue
                if even_test:
                    if test %2 != 0:
                        View.indication('the number must be an even number')
                        View.pause()
                        continue
                if test_element and not test_not_element:
                    if test in test_element:
                        return test
                    else:
                        continue
                if test_element and test_not_element:
                    if test in test_element and test not in test_not_element:
                        return test
                    else:
                        continue
                if not test_element and test_not_element:
                    if test not in test_not_element:
                        return test
                    else:
                        continue
                if test_range_element:
                    if test not in range(test_range_element):
                        continue
                    else:
                        return test
                else:
                    return test
            

