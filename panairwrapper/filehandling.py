"""This module provides tools for handling Panair input and output files.

The purpose of this module is to handle the formatting details of the Panair
input and output files. Thus, the user just has to specify the data or ask for
data and can forget about the details of formatting.

Example
-------
The following is code for generating an inputfile for a simple Panair case.

import file_handling
import numpy as np

# Get an InputFile object
inputfile = file_handling.InputFile()

# Specify the information for each required input block
inputfile.title("test case", "Ted Giblette")
inputfile.datacheck(0)
inputfile.symmetric(1, 0)
inputfile.mach(1.5)
inputfile.cases(1)
inputfile.anglesofattack(0., [-1., 0., 1.])
inputfile.yawangle(0., [-1., -1., -1.])
inputfile.printout(0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)

# The following are just empty arrays. In reality, these would contain
# coordinates for the points that describe the geometry.
network_points = np.zeros((3, 11, 3))
network_points_2 = np.zeros((3, 7, 3))
inputfile.points(2, 1, ['upper', 'lower'],
                 [network_points, network_points_2])
inputfile.trailingwakenetworks(2, 18, 0, ['left', 'right'], ['upper', 'lower'],
                               [3, 3], [10., 10], [0, 0])
inputfile.flowfieldproperties(1., 0.)

# Coordinates for points you want to collect off-body data at.
xyz_offbody_points = np.zeros((10, 3))
inputfile.xyzcoordinatesofoffbodypoints(10, xyz_offbody_points)

# Generate the inpufile
inputfile.write_inputfile("./test_input.INP")

Notes
-----
Since the functionality of Panair is quite large (much of which is not used
in common cases), the functionality of this module is being implemented on an
"as needed" basis. For example, not all input blocks available in Panair have
been implemented in the InputFile class. Adding something like this is fairly
straightforward. One would just need to refer to the Panair documentation,
figure out the appropriate formatting, and then follow the patterns used for
the other input blocks in the InputFile class to implement the new one.

This module does not remove the need of the user to understand the information
that's in the input and output files of the Panair.
Original documentation for Panair can be found at
http://www.pdas.com/panairrefs.html

"""
from collections import OrderedDict


class InputFile:
    """  """
    def __init__(self):
        self._input_dict = OrderedDict()

    def write_inputfile(self, filename):
        with open(filename, 'w') as f:
            for name, text in self._input_dict.items():
                f.write("$"+name+"\n")
                f.write(text)

    @staticmethod
    def _format_opt(number):
        fnumber = float(number)
        return '{0:<10}'.format(fnumber)

    @staticmethod
    def _format_str_opt(string):
        return '{0:<10}'.format(string)

    @staticmethod
    def _format_coord(coordinates):
        return '{0[0]:10f}{0[1]:10f}{0[2]:10f}'.format(coordinates)

    def title(self, title, info):
        self._input_dict["TITLE"] = title+"\n"+info+"\n"

    def datacheck(self, ndtchk):
        header = "=ndtchk\n"
        option = self._format_opt(ndtchk)+"\n"
        self._input_dict["DATACHECK"] = header+option

    def symmetric(self, xzpln, xypln):
        header = "=xzpln    xypln\n"
        options = self._format_opt(xzpln)+self._format_opt(xypln)+"\n"
        self._input_dict["SYMMETRIC"] = header+options

    def mach(self, amach):
        header = "=amach\n"
        value = self._format_opt(amach)+"\n"
        self._input_dict["MACH NUMBER"] = header+value

    def cases(self, nacase):
        header = "=nacase\n"
        option = self._format_opt(nacase)+"\n"
        self._input_dict["CASES"] = header+option

    def anglesofattack(self, alpc, alphas):
        header1 = "=alpc\n"
        input1 = self._format_opt(alpc)+"\n"
        header2 = "="
        input2 = ""

        for i, a in enumerate(alphas):
            header2 += "alpha("+str(i)+")  "
            input2 += self._format_opt(a)

        header2 += "\n"
        input2 += "\n"

        aoa_input = header1+input1+header2+input2

        self._input_dict["ANGLES OF ATTACK"] = aoa_input

    def yawangle(self, betc, betas):
        header1 = "=betc\n"
        input1 = self._format_opt(betc)+"\n"
        header2 = "="
        input2 = ""

        for i, b in enumerate(betas):
            header2 += "beta("+str(i)+")   "
            input2 += self._format_opt(b)

        header2 += "\n"
        input2 += "\n"

        beta_input = header1+input1+header2+input2

        self._input_dict["YAW ANGLE"] = beta_input

    def referencedata(self, xref, yref, zref, sref, bref, cref, dref):
        header1 = "=xref     yref      zref\n"
        input1 = self._format_opt(xref)
        input1 += self._format_opt(yref)
        input1 += self._format_opt(zref)+"\n"
        header2 = "=sref     bref      cref      dref\n"
        input2 = self._format_opt(sref)
        input2 += self._format_opt(bref)
        input2 += self._format_opt(cref)
        input2 += self._format_opt(dref)+"\n"

        ref_input = header1+input1+header2+input2

        self._input_dict["REFERENCE DATA"] = ref_input

    def printout(self, isings, igeomp, isingp, icontp, ibconp, iedgep,
                 ipraic, nexdgn, ioutpr, ifmcpr, icostp):
        header1 = "=isings   igeomp    isingp    icontp    ibconp    iedgep\n"
        input1 = self._format_opt(isings)+self._format_opt(igeomp)
        input1 += self._format_opt(isingp)+self._format_opt(icontp)
        input1 += self._format_opt(ibconp)+self._format_opt(iedgep)+"\n"
        header2 = "=ipraic   nexdgn    ioutpr    ifmcpr    icostp\n"
        input2 = self._format_opt(ipraic)+self._format_opt(nexdgn)
        input2 += self._format_opt(ioutpr)+self._format_opt(ifmcpr)
        input2 += self._format_opt(icostp)+"\n"

        printout = header1+input1+header2+input2

        self._input_dict["PRINTOUT CONTROL"] = printout

    def points(self, kn, kt, netnames, netpoints):
        header1 = "=kn\n"
        input1 = self._format_opt(kn)+"\n"
        header2 = "=kt\n"
        input2 = self._format_opt(kt)+"\n"
        points_input = header1+input1+header2+input2
        for i in range(int(kn)):
            points_input += self._gen_network_inp(netnames[i], netpoints[i])

        self._input_dict["POINTS kt="+str(kt)] = points_input

    def _gen_network_inp(self, netname, points):
        header = ("=nm       nn                                             " +
                  "    " + netname + "\n")
        nn, nm = points.shape[:2]
        values = self._format_opt(nm)+self._format_opt(nn)+"\n"
        network_input = header+values
        for i in range(int(nn)):
            for j in range(int(nm)):
                network_input += self._format_coord(points[i, j])

                if (j+1) % 2 is 0:
                    network_input += "\n"

            if nm % 2 is not 0:
                network_input += "\n"

        return network_input

    def trailingwakenetworks(self, kn, kt, matchw, netnames, inat,
                             insd, xwake, twake):
        header1 = "=kn\n"
        input1 = self._format_opt(kn)+"\n"
        header2 = "=kt       matchw\n"
        input2 = self._format_opt(kt)+self._format_opt(matchw)+"\n"
        wake_input = header1+input1+header2+input2
        for i in range(int(kn)):
            wake_input += self._gen_wake_inp(netnames[i], inat[i], insd[i],
                                             xwake[i], twake[i])

        self._input_dict["TRAILING matchw="+str(matchw)] = wake_input

    def _gen_wake_inp(self, netname, inat, insd, xwake, twake):
        header = ("=inat     insd      xwake     twake                      " +
                  "    " + netname + "\n")
        values = self._format_str_opt(inat) + self._format_opt(insd)
        values += self._format_opt(xwake) + self._format_opt(twake)+"\n"

        return header+values

    def flowfieldproperties(self, nflowv, tpoff):
        header = "=nflowv   tpoff     \n"
        values = self._format_opt(nflowv)+self._format_opt(tpoff)+"\n"

        self._input_dict["FLOW-FIELD PROPERTIES"] = header+values

    def xyzcoordinatesofoffbodypoints(self, isk1, points):
        header1 = "=isk1\n"
        input1 = self._format_opt(isk1)+"\n"
        header2 = "xof       yof       zof       xof       yof       zof\n"
        offbody_input = header1+input1+header2
        for i in range(int(isk1)):
            offbody_input += self._format_coord(points[i])
            if (i+1) % 2 is 0:
                offbody_input += "\n"
        if int(isk1) % 2 is not 0:
            offbody_input += "\n"

        self._input_dict["XYZ OF OFF-BODY POINTS"] = offbody_input
