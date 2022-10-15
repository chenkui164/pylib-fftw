import os
from setuptools import setup, Extension
from setuptools.command.build_clib import build_clib
from wheel.bdist_wheel import bdist_wheel as bdist_wheel_


class bdist_wheel(bdist_wheel_):
    def get_tag(self):
        _, _, plat_name = bdist_wheel_.get_tag(self)
        return 'py2.py3', 'none', plat_name

from sys import platform
from shutil import copyfile, copytree
import glob

FFTW3Version = '3.3.10'
name = 'pylib_fftw3'

des = "Python packaging of FFTW3 {version}".format(version=FFTW3Version)


class MyBuildCLib(build_clib):
    def run(self):
        try:
            import urllib.request as request
        except ImportError:
            import urllib as request
        # fname = "v{version}.tar.gz".format(version=FFTW3Version)
        fname = "fftw-{version}.tar.gz".format(version=FFTW3Version)
        print("Downloading FFTW3 version {}".format(FFTW3Version))
        request.urlretrieve("http://www.fftw.org/fftw-{version}.tar.gz".format(version=FFTW3Version), fname)
        import tarfile
        print("Extracting FFTW3 version {}".format(FFTW3Version))
        with tarfile.open(fname, "r:gz") as tar:
            tar.extractall()

        import subprocess
        print("Building FFTW3 version {}".format(FFTW3Version))
        if platform == "win32":
            builder = ["cmake", "--build", '.']
        else:
            builder = ['make', '-j2']

        try:
            os.makedirs(self.build_temp)
        except OSError:
            pass

        cwd = os.getcwd()
        os.chdir(self.build_temp)
        # this is clumsy <3
        guess_libplat = glob.glob(os.path.join(cwd, 'build', 'lib*'))[0]
        install_prefix = os.path.join(guess_libplat, 'pylib_fftw3')
        subprocess.check_call(["cmake",
                               '-DCMAKE_BUILD_TYPE=Release',
                               '-DBUILD_SHARED_LIBS=OFF',
                               os.path.join(cwd, 'fftw-{version}'.format(version=FFTW3Version)),
                               "-DCMAKE_INSTALL_PREFIX="+install_prefix])
        subprocess.check_call(builder)
        subprocess.check_call(["cmake", "--build", '.', '--target', 'install'])

        guess_libblas = glob.glob(os.path.join(install_prefix, 'lib*', '*fftw3*'))[0]
        target_libblas = guess_libblas.replace('fftw3', 'pylib_fftw3')
        copyfile(guess_libblas, os.path.basename(target_libblas))

        os.chdir(cwd)

setup(name=name,
      version='0.0.2',
      packages=[name],
      libraries=[(name, {'sources': []})],
      description=des,
      long_description='Binary distribution of FFTW3 static libraries',
      author='chenkui164',
      ext_modules=[Extension("pylib_fftw3.placeholder", ['pylib_fftw3/placeholder.c'])],
      cmdclass={'build_clib': MyBuildCLib,'bdist_wheel': bdist_wheel},
      options={'bdist_wheel':{'universal':True}}
      )

