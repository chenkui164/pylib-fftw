import os
import sys

if sys.platform == "win32":
    static_library = "fftw3.lib"
else:
    static_library = "libfftw3.a"

__dir__ = os.path.dirname(__file__)
include_dirs = os.path.join(__dir__, 'include'),
if os.path.isdir(os.path.join(__dir__, 'lib')):
    library_dir = os.path.join(__dir__, 'lib')
elif os.path.isdir(os.path.join(__dir__, 'lib64')):
    library_dir = os.path.join(__dir__, 'lib64')
else:
    raise RuntimeError("Unsupported library layout")
