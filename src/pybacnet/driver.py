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

import json
import re
import operator
import sys

from twisted.internet import threads, defer

from smap.driver import SmapDriver
from smap.util import periodicSequentialCall
from pybacnet import bacnet

def _get_class(name):
  cmps = name.split('.')
  assert len(cmps) > 1
  (mod_name, class_name) = ('.'.join(cmps[:-1]), cmps[-1])
  if mod_name in sys.modules:
      mod = sys.modules[mod_name]
  else:
      mod = __import__(mod_name, globals(), locals(), [class_name])
  return getattr(mod, class_name)

class BACnetDriver(SmapDriver):
    """Driver for polling BACnet points"""
    def setup(self, opts):
        bacnet.Init(opts.get('iface', 'eth0'), '47900')
        with open(opts.get('db'), 'r') as fp:
            self.db = json.load(fp)
        self.rate = int(opts.get('rate', 60))
        self.devices = map(re.compile, opts.get('devices', ['.*']))
        self.points = map(re.compile, opts.get('points', ['.*']))
        self.ffilter = _get_class(opts.get('filter')) if opts.get('filter') else None
        self.pathnamer = _get_class(opts.get('pathnamer')) if opts.get('pathnamer') else None
        for (dev, obj, path) in self._iter_points():
            unit = str(obj['unit']).strip()
            if unit.isdigit():
                unit = str(bacnet.type_str(int(unit)))
            self.add_timeseries(path, unit, data_type='double')

    @staticmethod
    def _matches(s, pats):
        return len(filter(None, map(lambda p: p.match(s), pats))) > 0

    def get_path(self, dev, obj):
        if self.pathnamer:
            path = str(self.pathnamer(dev['name'], obj['name']))
        else:
            path = str('/' + dev['name'] + '/' + obj['name'])
        return (dev, obj, path)

    def _iter_points(self):            
        for dev in self.db:
            if self.ffilter:
                for obj in dev['objs']:
                    if self.ffilter(dev['name'], obj['name']):
                        yield self.get_path(dev, obj)
            else: 
                if not self._matches(dev['name'], self.devices): continue
                for obj in dev['objs'][1:]:
                    if not self._matches(obj['name'], self.points): continue
                    yield self.get_path(dev, obj)

    def start(self):
        self.caller = periodicSequentialCall(self.update)
        self.caller.start(self.rate)

    @defer.inlineCallbacks
    def update(self):
        for (dev, obj, path) in self._iter_points():
            try:
                val = yield threads.deferToThread(bacnet.read_prop,
                                                  dev['props'],
                                                  obj['props']['type'],
                                                  obj['props']['instance'],
                                                  bacnet.PROP_PRESENT_VALUE,
                                                  -1)
            except IOError:
                pass
            else:
                self._add(path, float(val))
