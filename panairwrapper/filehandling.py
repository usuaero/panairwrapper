"""This module provides tools for handling Panair input and output files.

The purpose of this module is to handle the formatting details of the Panair
input and output files. Thus, the user just has to specify the data or ask for
data and can forget about the details of formatting.

Notes
-----
Since the functionality of Panair is quite large (much of which is not used
in common cases), the functionality of this module is being implemented on an
"as needed" basis.

This module does not remove the need of the user to understand the information
that's in the input and output files of the Panair.
Original documentation for Panair can be found at
http://www.pdas.com/panairrefs.html

"""
from collections import OrderedDict
import numpy as np
from math import copysign


class InputFile:
    """Handles the formatting of a Panair input file.

    Data for individual Input Blocks of the inputfile is specified via a member
    function that corresponds to the input block title. Once all of the
    required data has been specified in this manner, the inputfile may be
    generated using the write_inputfile member function.

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
    inputfile.trailingwakenetworks(2, 18, 0, ['left', 'right'],
                                   ['upper', 'lower'],
                                   [3, 3], [10., 10], [0, 0])
    inputfile.flowfieldproperties(1., 0.)

    # Coordinates for points you want to collect off-body data at.
    xyz_offbody_points = np.zeros((10, 3))
    inputfile.xyzcoordinatesofoffbodypoints(10, xyz_offbody_points)

    # Generate the inpufile
    inputfile.write_inputfile("./test_input.INP")

    Notes
    -----
    Not all input blocks available in Panair have been implemented in the
    InputFile class. Adding something like this is fairly straightforward
    however. One would just need to refer to the Panair documentation, figure
    out the appropriate formatting, and then follow the patterns used for
    the other input blocks this class to implement the new one.
    """
    def __init__(self):
        self._input_dict = OrderedDict()

    def write_inputfile(self, filename):
        with open(filename, 'w') as f:
            for name, text in self._input_dict.items():
                f.write("$"+name+"\n")
                f.write(text)
            f.write("$end")

    @staticmethod
    def _format_opt(number):
        fnumber = float(number)
        return '{0:<10}'.format(fnumber)

    @staticmethod
    def _format_str_opt(string):
        return '{0:<10}'.format(string)

    def _format_coord(self, coordinates):
        precision = [6, 6, 6]
        for i, c in enumerate(coordinates):
            precision[i] = self._fixed_width_precision(c)

        s = ('{0[0]:<10.'+str(precision[0])+'f}' +
             '{0[1]:<10.'+str(precision[1])+'f}' +
             '{0[2]:<10.'+str(precision[2])+'f}')

        return s.format(coordinates)

    @staticmethod
    def _fixed_width_precision(number):
        precision = 8
        if copysign(1, number) < 0:
            precision -= 1
        if abs(number) >= 10:
            precision -= 1
        if abs(number) >= 100:
            precision -= 1
        if abs(number) >= 1000:
            precision -= 1
        if abs(number) >= 10000:
            precision -= 1
        if abs(number) >= 100000:
            raise RuntimeError("formatting not implemented")

        return precision

    def _format_header(self, labels):
        header = ""
        for i, l in enumerate(labels):
            if i == 0:
                header += self._format_str_opt("="+l)
            else:
                header += self._format_str_opt(l)
        header += "\n"

        return header

    def _format_inputline(self, values):
        inputs = ""
        for v in values:
            inputs += self._format_opt(v)
        inputs += "\n"

        return inputs

    def title(self, title, info):
        self._input_dict["TITLE"] = title+"\n"+info+"\n"

    def datacheck(self, ndtchk):
        # header = "=ndtchk\n"
        header = self._format_header(["ndtchk"])
        option = self._format_inputline([ndtchk])
        self._input_dict["DATACHECK"] = header+option

    def symmetric(self, xzpln, xypln):
        header = self._format_header(["xzpln", "xypln"])
        options = self._format_inputline([xzpln, xypln])
        self._input_dict["SYMMETRIC"] = header+options

    def mach(self, amach):
        header = self._format_header(["amach"])
        value = self._format_inputline([amach])
        self._input_dict["MACH NUMBER"] = header+value

    def cases(self, nacase):
        header = self._format_header(["nacase"])
        option = self._format_inputline([nacase])
        self._input_dict["CASES"] = header+option

    def anglesofattack(self, alpc, alphas):
        header1 = self._format_header(["alpc"])
        input1 = self._format_inputline([alpc])
        # generate headers for alphas based on number
        headers_2 = []
        for i, a in enumerate(alphas):
            headers_2.append("alpha("+str(i)+")")
        header2 = self._format_header(headers_2)
        input2 = self._format_inputline(alphas)

        aoa_input = header1+input1+header2+input2

        self._input_dict["ANGLES OF ATTACK"] = aoa_input

    def yawangle(self, betc, betas):
        header1 = self._format_header(["betc"])
        input1 = self._format_inputline([betc])
        # generate headers for betas based on number
        headers_2 = []
        for i, b in enumerate(betas):
            headers_2.append("beta("+str(i)+")")
        header2 = self._format_header(headers_2)
        input2 = self._format_inputline(betas)

        beta_input = header1+input1+header2+input2

        self._input_dict["YAW ANGLE"] = beta_input

    def referencedata(self, xref, yref, zref, sref, bref, cref, dref):
        header1 = self._format_header(["xref", "yref", "zref"])
        input1 = self._format_inputline([xref, yref, zref])
        header2 = self._format_header(["sref", "bref", "cref", "dref"])
        input2 = self._format_inputline([sref, bref, cref, dref])

        ref_input = header1+input1+header2+input2

        self._input_dict["REFERENCE DATA"] = ref_input

    def printout(self, isings, igeomp, isingp, icontp, ibconp, iedgep,
                 ipraic, nexdgn, ioutpr, ifmcpr, icostp):
        header1 = self._format_header(["isings", "igeomp", "isingp",
                                       "icontp", "ibconp", "iedgep"])
        input1 = self._format_inputline([isings, igeomp, isingp,
                                         icontp, ibconp, iedgep])
        header2 = self._format_header(["ipraic", "nexdgn", "ioutpr",
                                       "ifmcpr", "icostp"])
        input2 = self._format_inputline([ipraic, nexdgn, ioutpr,
                                         ifmcpr, icostp])

        printout = header1+input1+header2+input2

        self._input_dict["PRINTOUT CONTROL"] = printout

    def points(self, kn, kt, netnames, netpoints):
        header1 = self._format_header(["kn"])
        input1 = self._format_inputline([kn])
        header2 = self._format_header(["kt"])
        input2 = self._format_inputline([kt])
        points_input = header1+input1+header2+input2
        for i in range(int(kn)):
            points_input += self._gen_network_inp(netnames[i], netpoints[i])

        self._input_dict["POINTS kt="+str(kt)] = points_input

    def _gen_network_inp(self, netname, points):
        header = ("=nm       nn                                             " +
                  "    " + netname + "\n")
        nn, nm = points.shape[:2]
        values = self._format_inputline([nm, nn])
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
        header1 = self._format_header(["kn"])
        input1 = self._format_inputline([kn])
        header2 = self._format_header(["kt", "matchw"])
        input2 = self._format_inputline([kt, matchw])
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
        header = self._format_header(["nflowv", "tpoff"])
        values = self._format_inputline([nflowv, tpoff])

        self._input_dict["FLOW-FIELD PROPERTIES"] = header+values

    def xyzcoordinatesofoffbodypoints(self, isk1, points):
        header1 = self._format_header(["isk1"])
        input1 = self._format_inputline([isk1])
        header2 = self._format_header(["xof", "yof", "zof",
                                       "xof", "yof", "zof"])
        offbody_input = header1+input1+header2
        for i in range(int(isk1)):
            offbody_input += self._format_coord(points[i])
            if (i+1) % 2 is 0:
                offbody_input += "\n"
        if int(isk1) % 2 is not 0:
            offbody_input += "\n"

        self._input_dict["XYZ OF OFF-BODY POINTS"] = offbody_input


class OutputFile:
    """Handles the parsing of Panair output file.

    Data for the output blocks listed in the panair.out file generated
    by Panair is parsed and then made available in numpy arrays.
    """
    def __init__(self, directory):
        self._directory = directory

    def _get_block(self, block_name):
        # retrieves lines inside block
        begin_flag = "0*b*"+block_name
        end_flag = "0*e*"+block_name
        with open(self._directory+"panair.out") as f:
            lines = f.readlines()
            count = 0
            while begin_flag not in lines[count]:
                count += 1
            front = count+1
            while end_flag not in lines[count]:
                count += 1
            back = count

            return lines[front:back]

    @staticmethod
    def _lines_to_numpy(data_lines):
        # converts lines that hold column data into numpy array
        array = [[float(val) for val in line.split()] for line in data_lines]

        return np.array(array)

    def get_offbody_data(self):
        block_lines = self._get_block("off-body")
        data_lines = block_lines[6:]

        data = self._lines_to_numpy(data_lines)

        return data
