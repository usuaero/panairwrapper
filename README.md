# panairwrapper

This package provides a Python wrapper for the Panair program.

The primary purpose of panairwrapper is to provide a programmatic
interface) for Panair. This is done through the Panair interface available to
us, the input and output files. Thus, this module handles all of the formatting
details of generating a Panair inputfile and extracting data from the
outputfiles.

Additionaly, this module seeks to provide sane defaults for the many settings
available in Panair. This allows a user to start out simple and then dig into
the Panair settings as necessary for special cases.

By providing a programmatic interface to running Panair cases, this module
facilitates the creation of interfaces between Panair and other codes. For
example, another code can be used for generating/specifying a geometry
description or for postprocessing or visualizing results.


The following code demonstrates how panairwrapper might be used in a 
Python script:

```python
import panairwrapper.panairwrapper as panair

# generate and run Panair case
axie_case = panair.Case("NASA25D AXIE",
                        description="Ted Giblette, USU AEROLAB")

axie_case.set_aero_state(mach=1.6, alpha=0., beta=0.)

# network points and off-body points are passed in as numpy arrays
axie_case.add_network("front", network_points_0)
axie_case.add_network("front_mid", network_points_1)
axie_case.add_network("back_mid", network_points_2)
axie_case.add_network("back", network_points_3)

axie_case.add_offbody_points(off_body_points)

results = axie_case.run()

offbody_data = results.get_offbody_data()
```

## Notes

Although simplifying to some degree the use of Panair, this module does
not remove the need of the user to understand the proper use of the Panair
program. Original documentation for Panair can be found at
http://www.pdas.com/panairrefs.html
It should also be noted that this is a work in progress so not all of the
functionaltity of Panair has been built into this interface. Feel free to
request or contribute any desired additions!

The use of this module is obviously based on Panair already being
installed on your system. Source code can be found at
http://www.pdas.com/panair.html
and is simple to install. Once installed the executable (should be 'panair')
needs to be copied into the folder where panairwrapper is being used. 

The default precision included in the Panair output files isn't very good
for getting collecting off-body data. This can be remedied however by making
a few small modifications to the source code before compiling panair.
Specifically, change the formatting found at lines 38834-38836 in panair.f90.

For example, change the following
```fortran
1001 format (1x,i4,i5     ,4x ,3f11.4                                  &
     & ,4x  ,3f11.4                                                     &
     & ,2x  ,f11.4          ,2x  ,f11.4           ,f11.4)
```
to
```fortran
1001 format (1x,i4,i5     ,4x ,3f13.8                                  &
     & ,4x  ,3f13.8                                                     &
     & ,2x  ,f13.8          ,2x  ,f13.8    ,1x       ,f13.8)
```

Additionaly, an approximately 5X speed up of Panair was obtained on our
systems by compiling panair with the '-O3 -ffast-math' flags (gfortran compiler)
over no optimization flags.

## Documentation

See doc strings in code. 

## Installation

Run either of the following commands in the main directory.

'pip install .'
or
'python setup.py install'

If developing, instead use

'pip install -e .'
or
'python setup.py develop'

It is recommended that pip is used instead of invoking setup.py directly.

### Prerequisites

Panair must be downloaded and installed and the resulting executable 
copied into the folder where code is being run.

### Getting the Source Code

The source code can be found at [https://github.com/usuaero/panairwrapper](https://github.com/usuaero/panairwrapper)

You can either download the source as a ZIP file and extract the contents, or 
clone the panairwrapper repository using Git. If your system does not already have a 
version of Git installed, you will not be able to use this second option unless 
you first download and install Git. If you are unsure, you can check by typing 
`git --version` into a command prompt.

#### Downloading source as a ZIP file

1. Open a web browser and navigate to [https://github.com/usuaero/panairwrapper](https://github.com/usuaero/panairwrapper)
2. Make sure the Branch is set to `Master`
3. Click the `Clone or download` button
4. Select `Download ZIP`
5. Extract the downloaded ZIP file to a local directory on your machine

#### Cloning the Github repository

1. From the command prompt navigate to the directory where MachUp will be installed
2. `git clone https://github.com/usuaero/panairwrapper`

## Testing
Unit tests are implemented using the pytest module and are run using the following command.

'python3 -m pytest test/'

##Support
Contact doug.hunsaker@usu.edu with any questions.

##License
This project is licensed under the ??? license. See LICENSE file for more information. 
