import glob
import os
import pytest
from antlr4.error.Errors import ParseCancellationException

from parse.quickparse import quickparse
from tests.file_helper import all_tre_files

tests = all_tre_files(fail_files = [os.path.join('..', 'experiments', 'spec_10_noparse.tre')])


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
        with pytest.raises(ParseCancellationException):
            print(file_path)
            print(quickparse(file_path).getText())

    else:
        # good test cases
        print(file_path)
        print(quickparse(file_path).getText())



