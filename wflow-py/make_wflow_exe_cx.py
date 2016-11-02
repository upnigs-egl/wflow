import sys
from cx_Freeze import setup, Executable, hooks
from _version import *
import ctypes,glob,os,shutil
import matplotlib
import scipy

target = 'openda'

import sys

includefiles_list=[]
scipy_path = os.path.dirname(scipy.__file__)
includefiles_list.append(scipy_path)


def load_scipy_patched(finder, module):
    """the scipy module loads items within itself in a way that causes
        problems without the entire package and a number of other subpackages
        being present."""
    finder.IncludePackage("scipy._lib")  # Changed include from scipy.lib to scipy._lib
    finder.IncludePackage("scipy.misc")

hooks.load_scipy = load_scipy_patched

def mkdatatuples(thelist,destdir="."):
    """
    input list of input files output lis list of tuples including destination
    :param list:
    :return:
    """
    ret = []
    for item in thelist:
        destfile = os.path.join(destdir,os.path.basename(item))
        ret.append((item,destfile))
    return ret

data_files = ['packages.txt']
os.system('conda list' + ">" + os.path.join('packages.txt'))
# matplolib data files


mpl =  matplotlib.get_py2exe_datafiles()

mplfiles = []
for mpldir in mpl:
    ddir = os.path.join('mpl-data',os.path.basename(mpldir[0]))
    data_files.extend(mkdatatuples(mpldir[1],destdir=ddir))


# pcraster dll's
ddir = "c:/pcraster/lib/"
data_files.extend(mkdatatuples(glob.glob(ddir + "/*.dll"),destdir='.'))

# GDAL data files
gdaldata = os.getenv("GDAL_DATA")
data_files.extend(mkdatatuples(glob.glob(gdaldata + "/*.*"),destdir='gdal-data'))


nrbits = str(ctypes.sizeof(ctypes.c_voidp) * 8)
#includes = ['wflow.wflow_bmi','wflow.wflow_w3ra','wflow.wflow_bmi_combined','bmi','bmi.wrapper',"pcraster","osgeo.ogr"]

thename = "Wflow"+MVERSION+'-'+nrbits

packages = ["osgeo"]


if target == 'openda':
    includes = ['wflow.wflow_bmi','wflow.wflow_w3ra','wflow.wflow_bmi_combined']
    packages.append('openda_bmi')
else:
    includes = ['wflow.wflow_bmi', 'wflow.wflow_w3ra', 'wflow.wflow_bmi_combined']

options = { "includes": includes, "packages": packages,'include_files': data_files, "build_exe": thename,'excludes': ['collections.abc']}
base=None



if target == 'openda':
    import thrift
    executables = [
        Executable('Scripts/pcr2netcdf.py', base=base),
        Executable('Scripts/bmi2runner.py', base=base),
        Executable('openda_bmi/thrift_bmi_raster_server.py', base=base),
        Executable('Scripts/wflow_prepare_step2.py', base=base),
        Executable('Scripts/wflow_prepare_step1.py', base=base),
        Executable('Scripts/wflow_sbm_rtc.py', base=base),
        Executable('wflow/wflow_topoflex.py', base=base),
        Executable('wflow/wflow_sbm.py', base=base),
        Executable('wflow/wflow_adapt.py', base=base),
        Executable('wflow/wflow_w3ra.py', base=base),
        Executable('wflow/wflow_delwaq.py', base=base),
        Executable('wflow/wflow_wave.py', base=base),
        Executable('wflow/wflow_gr4.py', base=base),
        Executable('wflow/wflow_floodmap.py', base=base),
        Executable('wflow/wflow_hbv.py', base=base)
    ]
else:
    executables = [
        Executable('Scripts/pcr2netcdf.py', base=base),
        Executable('Scripts/bmi2runner.py', base=base),
        Executable('Scripts/wflow_prepare_step2.py', base=base),
        Executable('Scripts/wflow_prepare_step1.py', base=base),
        Executable('Scripts/wflow_sbm_rtc.py', base=base),
        Executable('wflow/wflow_topoflex.py', base=base),
        Executable('wflow/wflow_sbm.py', base=base),
        Executable('wflow/wflow_adapt.py', base=base),
        Executable('wflow/wflow_w3ra.py', base=base),
        Executable('wflow/wflow_delwaq.py', base=base),
        Executable('wflow/wflow_wave.py', base=base),
        Executable('wflow/wflow_gr4.py', base=base),
        Executable('wflow/wflow_floodmap.py', base=base),
        Executable('wflow/wflow_hbv.py', base=base)
    ]

setup(name='wflow',
      version=NVERSION,
      description='Wflow',
      options={"build_exe" : options},
      executables=executables,
      )