"""Tests the file handling model."""
# pylint: disable=redefined-outer-name

import pytest
import filecmp
import numpy as np
import panairwrapper.filehandling as fh


TESTFILE_DIR = "./test/testfiles/"


def test_inputfile():

    inputfile = fh.InputFile()

    inputfile.title("test case", "Ted Giblette")
    inputfile.datacheck(0)
    inputfile.symmetric(1, 0)
    inputfile.mach(1.5)
    inputfile.cases(1)
    inputfile.anglesofattack(0., [-1., 0., 1.])
    inputfile.yawangle(0., [-1., -1., -1.])
    inputfile.printout(0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)

    network_points = np.zeros((3, 11, 3))
    network_points_2 = np.zeros((3, 7, 3))
    inputfile.points(2, 1, ['upper', 'lower'],
                     [network_points, network_points_2])
    inputfile.trailingwakenetworks(2, 18, 0, ['left', 'right'],
                                   ['upper', 'lower'],
                                   [3, 3], [10., 10], [0, 0])
    inputfile.flowfieldproperties(1., 0.)
    xyz_offbody_points = np.zeros((10, 3))
    inputfile.xyzcoordinatesofoffbodypoints(10, xyz_offbody_points)

    newfilename = TESTFILE_DIR+"test_input.INP"
    reffilename = TESTFILE_DIR+"inputfile.REF"

    inputfile.write_inputfile(newfilename)

    assert filecmp.cmp(newfilename, reffilename)


def test_read_cp_data():
    # tests the function for parsing control point data out of panair.out
    output = fh.OutputFiles(TESTFILE_DIR)
    output._output_all = True

    data = output.generate_vtk()

    assert False
