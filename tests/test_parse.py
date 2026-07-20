import os
import pytest

from parse.SyntaxError import TREParseError
from parse.quickparse import quickparse
from tests.file_helper import all_tre_files

_E = os.path.join(os.path.dirname(__file__), '..', 'experiments')
tests = all_tre_files(fail_files = [os.path.join(_E, 'spec_10_noparse.tre')])


@pytest.mark.parametrize("file_path, expected_to_fail", tests)
def test_quickparse(file_path, expected_to_fail):
    """
    Just a quick & dirty test whether it can parse all the .tre files.
    :param file_path: Path to the .tre file
    :param expected_to_fail: Boolean indicating if the test is expected to fail
    :return:
    """
    if expected_to_fail:
        # bad test cases that should fail
        with pytest.raises(TREParseError):
            print(file_path)
            print(quickparse(file_path).getText())

    else:
        # good test cases
        print(file_path)
        print(quickparse(file_path).getText())



