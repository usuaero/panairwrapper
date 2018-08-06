""" """
import pytest
import os
import platform

import panairwrapper

TESTFILE_DIR = os.path.join(os.path.dirname(__file__), 'testfiles')


PANAIR_EXE = 'panair'
if platform.system() == 'Windows':
    PANAIR_EXE = 'panair.exe'

@pytest.fixture
def empty_case():
    # setup

    """Construct a PanairWrapper for an empty case with no networks."""
    panair_case = panairwrapper.PanairWrapper("empty_case", TESTFILE_DIR,
                                              exe=PANAIR_EXE)

    yield panair_case

    # tear down
    panair_case.clean_up()


def test_generate_dir(empty_case):
    empty_case._generate_dir(True)

    assert os.path.isdir(os.path.join(TESTFILE_DIR, "panair_files"))
    assert os.path.isfile(os.path.join(TESTFILE_DIR, "panair_files", PANAIR_EXE))


