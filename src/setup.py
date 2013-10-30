"""
This file is part of pybacnet.

pybacnet is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pybacnet is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pybacnet.  If not, see <http://www.gnu.org/licenses/>.
"""
"""
Copyright (c) 2013 Building Robotics, Inc. 
"""
"""
@author Stephen Dawson-Haggerty <steve@buildingrobotics.com>
"""

import os
from distutils.core import setup, Extension

inc_dir = ['bacnet-stack-0.6.0/include', 
           'bacnet-stack-0.6.0/demo/object',
           'bacnet-stack-0.6.0/ports/linux']

prefix = os.path.dirname(os.path.abspath(__file__))
inc_dir = [os.path.join(prefix, dir) for dir in inc_dir]
lib_path = os.path.join(prefix, 'bacnet-stack-0.6.0/lib')
bacnet_module = Extension('pybacnet._bacnet',
  sources=['pybacnet/bacnet.c', 'pybacnet/bacnet.i'],
  swig_opts=['-I' + os.path.join(prefix, 'bacnet-stack-0.6.0/include')],
  libraries=['bacnet'],
  library_dirs=[lib_path],
  include_dirs=inc_dir)

setup(name="pybacnet",
      version="1.0",
      description="sMAP BACnet support",
      author="Stephen Dawson-Haggerty",
      author_email="steve@buildingrobotics.com",
      url="https://github.com/BuildingRobotics/pybacnet",
      license="GPLv3",
      packages=[
        "pybacnet", 
        ],
      requires=["smap", ],
      ext_modules=[
        bacnet_module,
        ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        ]
      )
