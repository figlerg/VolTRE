import os
import pytest
from antlr4.error.Errors import ParseCancellationException

from misc.disambiguate import disambiguate
from parse.quickparse import quickparse
from tests.file_helper import all_tre_files
from sample.sample import sample

_E = os.path.join(os.path.dirname(__file__), '..', 'experiments')
tests = all_tre_files(ignore_files = [os.path.join(_E, 'spec_10_noparse.tre'),
                                      os.path.join(_E, 'spec_08_renaming.tre'),
                                      os.path.join(_E, 'spec_07_intersection.tre'),
                                      os.path.join(_E, 'spec_12_intersection.tre'),
                                      ])


@pytest.mark.parametrize("file_path, expected_to_fail", tests)
def test_disambiguate(file_path, expected_to_fail):
    """
    Testing whether disambiguate function runs at all on the applicable cases.
    TODO also test whether it creates ambiguous expressions, maybe by sampling and using  match.py.
    :param file_path: Path to the .tre file
    :param expected_to_fail: Boolean indicating if the test is expected to fail
    :return:
    """

    # i only input good testcases here
    print(file_path)

    res = disambiguate(quickparse(file_path))
    print(res)

    # TODO maybe I can design a heuristic test of whether it is ambiguous? sampling and nr of matches?
    #   (but it is hard to know which expressions necessarily have a volume or can be vanilla sampled)






