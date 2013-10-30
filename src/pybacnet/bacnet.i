/**************************************************************************
 * This file is part of pybacnet.
 * 
 * pybacnet is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * pybacnet is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with pybacnet.  If not, see <http://www.gnu.org/licenses/>.
 *
 *********************************************************************/
/*
 * Copyright (c) 2013 Building Robotics, Inc.
 */
%module bacnet
%{
#include "bacenum.h"
void Init(char *interface, char *port);
PyObject *whois(unsigned int timeout_seconds);
PyObject *read_prop(PyObject *dev, uint32_t object_type, uint32_t object_instance, uint32_t object_property, int32_t array_index);
PyObject *write_prop(PyObject *dev, uint32_t object_type, uint32_t object_instance, uint32_t object_property, uint8_t property_tag, PyObject *val_str, uint8_t priority);
const char * type_str(unsigned index);
const char * prop_str(unsigned index);
const char * unit_str(unsigned index);
%}
%include "stdint.i"
%include "bacenum.h"
void Init(char *interface, char *port);
PyObject *whois(unsigned int timeout_seconds);
PyObject *read_prop(PyObject *dev, uint32_t object_type, uint32_t object_instance, uint32_t object_property, int32_t array_index = -1);
PyObject *write_prop(PyObject *dev, uint32_t object_type, uint32_t object_instance, uint32_t object_property, uint8_t property_tag, PyObject *val_str, uint8_t priority = 16);

const char * type_str(unsigned index);
const char * prop_str(unsigned index);
const char * unit_str(unsigned index);

