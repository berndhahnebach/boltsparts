# coding=utf8
#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import blt
import yaml
import unittest
from errors import *

class TestClass(unittest.TestCase):
	def setUp(self):
		self.cl = yaml.load("""
id: roundBattery
names:
  - name:
      safe: roundBattery 
      nice: Round Batteries
    labeling:
      nice: "%(T)s Battery"
    description: Most common round single cell battery sizes
  - name: Common Batteries
    labeling:
      safe: "%(T)s_Battery"
      nice: "%(T)s Battery"
    description: Most common round single cell battery sizes
standards:
  - body: IEC
    standard: IEC 60086
    suffix:
      safe: Cat1
      nice: Category 1
    labeling:
      nice: "IEC60086 Cat 1 Battery %(T)s"
    description: Cylindrical cells with protruding positive and recessed or flat negative terminals.
parameters:
  free: [T]
  defaults: {T: "AAA"}
  types:
    T: Table Index
    h: Length (mm)
    d: Length (mm)
  description:
    T: Type Code
    h: height
    d: diameter
  tables:
     index: T
     columns: [h,d]
     data:
       "AAA" : [44.5,10.5]
       "AA" : [50.5,14.5]
       "C" : [50,26.2]
       "D" : [61.5,34.2]
       "1/2AA" : [24,14.5]
       "AAAA" : [42.5,8.3]
       "A" : [50, 17]
       "N" : [30.2, 12]
       "Sub-C" : [42.9, 22.2]
source: http://en.wikipedia.org/wiki/List_of_battery_sizes
""")

	def test_class(self):
		res = blt.Class(self.cl)
		self.assertEqual(res.source,'http://en.wikipedia.org/wiki/List_of_battery_sizes')
		self.assertEqual(res.id,'roundBattery')

	def test_classname(self):
		res = []
		for cn in self.cl['names']:
			res.append(blt.ClassName(cn))

		self.assertEqual(len(res),2)

		#use noop substitution
		self.assertEqual(res[0].labeling.get_safe_name({'T' : '%(T)s'}),'%(T)s_Battery')
		self.assertEqual(res[1].labeling.get_safe_name({'T' : '%(T)s'}),'%(T)s_Battery')

	def test_standardname(self):
		res = []
		for sn in self.cl['standards']:
			res.append(blt.StandardName(sn))

		self.assertEqual(len(res),1)
		self.assertEqual(res[0].standard.get_safe_name(),'IEC60086')
		self.assertEqual(res[0].standard.get_nice_name(),'IEC 60086')
		self.assertEqual(res[0].suffix.get_safe_name(),'Cat1')
		self.assertEqual(res[0].suffix.get_nice_name(),'Category 1')

class MockDesignation(blt.DesignationMixin):
	def __init__(self,id,subids=[]):
		self.id = id
		self.subids = subids
	def get_id(self):
		return self.id
	def all_standards_single(self):
		for sid in self.subids:
			yield MockDesignation(sid)
	def all_names_single(self):
		for sid in self.subids:
			yield MockDesignation(sid)
	def contains_standard_single(self,id):
		return id in self.subids
	def contains_name_single(self,id):
		return id in self.subids
	def get_standard_single(self,id):
		if not id in self.subids:
			raise KeyError("Key not found")
		return MockDesignation(id)

#TODO: slow?
class TestRepository(unittest.TestCase):
	def setUp(self):
		self.repo = blt.Repository("test_blt")

	def test_repository(self):
		self.assertTrue("hexagonthinnut1" in self.repo.classes)
		self.assertTrue('nut' in self.repo.collections)
		self.assertEqual(len(self.repo.classes),11)
		self.assertEqual(len(self.repo.collections),2)

	def test_accessors(self):
		self.assertEqual(len([1 for n in self.repo.iternames()]),7)
		self.assertEqual(len([1 for n in self.repo.iterstandards()]),14)

	def test_bodies(self):
		self.assertEqual(len(self.repo.bodies),5)
		self.assertTrue('DIN' in self.repo.bodies)


if __name__ == '__main__':
	unittest.main()


