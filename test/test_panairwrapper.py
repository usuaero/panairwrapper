""" """
import pytest
import os

import panairwrapper

TESTFILE_DIR = os.path.join(os.path.dirname(__file__), 'testfiles')


@pytest.fixture
def empty_case():
    # setup
    """Construct a PanairWrapper for an empty case with no networks."""
    panair_case = panairwrapper.PanairWrapper("empty_case", TESTFILE_DIR)

    yield panair_case

    # tear down
    panair_case.clean_up()


def test_generate_dir(empty_case):
    empty_case._generate_dir(True)

    assert os.path.isdir(os.path.join(TESTFILE_DIR, "panair_files"))
    assert os.path.isfile(os.path.join(TESTFILE_DIR, "panair_files", "panair"))


