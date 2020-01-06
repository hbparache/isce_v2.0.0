#!/usr/bin/env python3
from __future__ import print_function
import math
import isceobj.Planet.AstronomicalHandbook as AstronomicalHandbook
from isceobj.Planet.Ellipsoid import Ellipsoid


class Planet(object):
    """
    A class to represent a planet.
    The parameters maintained internally are the following:

    elp = an ellipsoid model of class Ellipsoid

    GM  = Planet mass in units of acceleration * distance**2 --- 
    dividing by distance**2 from the center of the planet gives the
    gravitational acceleration at that distance and 
    dividing by the distance gives the gravitational potential field
    monopole term at that distance

    spin = radian frequency of the planet's spin
    """
    #modified the constructor so it takes the ellipsoid model. this way it
    #does not to be hardcoded to WGS-84. 
    #also ellipsoid as been modified so it has the model attribute
    def __init__(self, name, ellipsoidModel=None):
        self._name = name
        if ellipsoidModel is None:
            if name == 'Earth':
                ellipsoidModel = 'WGS-84'
            else:
                elliposoidModel = 'default'
                ########## TO BE DONE in AstronomicalHandbook.py:
                # define a generic model called
                # default that just maps the name of the planet to the correspoding
                # axis and eccentricity 
                #######################
                print(
                    'At the moment  there is no default ellipsoid defined for the planet',
                    name)
                raise NotImplementedError
            pass
        if name in AstronomicalHandbook.PlanetsData.names:
            self._ellipsoid = (
                Ellipsoid(
                    *AstronomicalHandbook.PlanetsData.ellipsoid[
                        name
                        ][ellipsoidModel],
                     model=ellipsoidModel)
                )
            self.GM = AstronomicalHandbook.PlanetsData.GM[name]
            self.spin = (
                2.0*math.pi/
                AstronomicalHandbook.PlanetsData.rotationPeriod[name]
                )
        else:
            self._ellipsoid = Ellipsoid()
            self.GM = 1.0
            self.spin = 1.0
            pass
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = {'NAME': ['name', 'str', 'mandatory'],
                                      'GM': ['GM','float','mandatory'],
                                      'SPINRATE': ['spin','float','mandatory']}
        return None
    
    @property
    def name(self):
        """Name of the planet"""
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
        return None

    def set_name(self,name):
        if not isinstance(name,basestring):
            raise ValueError("attempt to instantiate a planet with a name %s that is not a string" % name)
        self.name = name
        return None
    
    def get_name(self):
        return self.name

    @property
    def ellipsoid(self):
        """Ellipsoid model of the planet.  See Ellipsoid class."""        
        return self._ellipsoid
    @ellipsoid.setter
    def ellipsoid(self, elp):
        self._ellipsoid = elp
        return None
    
    def get_elp(self):
        return self.ellipsoid

    @property
    def GM(self):
        """Mass of planet times Newton's gravitational constant in m**3/s**2"""
        return self._GM
    @GM.setter
    def GM(self, GM):
        try:
            self._GM = float(GM)
        except (TypeError, ValueError):
            raise ValueError(
                "invalid use of non-numeric object %s to set GM value "
                %
                str(GM)
                ) 
        return None
    
    def get_GM(self):
        return self.GM

    def set_GM(self, GM):
        self.GM = GM
        pass

    @property
    def spin(self):
        return self._spin
    @spin.setter
    def spin(self, spin):
        try:
            self._spin = float(spin)
        except (ValueError, TypeError):
            raise ValueError(
                "invalid use of non-numeric object %s to set spin " % spin
                )
        pass
        
    def get_spin(self):
        return self.spin
    
    def set_spin(self, spin):
        self.spin = spin

    @property
    def polar_axis(self):
        return self._polar_axis
    @polar_axis.setter
    def polar_axis(self, vector):
        """Give me a vector that is parallel to my spin axis"""
        from isceobj.Util.geo.euclid import Vector
        if not isinstance(vector, Vector):
            try:
                vector = Vector(*vector)
            except Exception:
                raise ValueError(
                    "polar axis must a Vector or length 3 container"
                    )
            pass
        self._polar_axis = vector.hat()
        return None

    @property
    def ortho_axis(self):
        return self._ortho_axis

    @property
    def primary_axis(self):
        return self._primary_axis

    @primary_axis.setter
    def primary_axis(self, vector):
        """Give me a vector in your coordinates that is orthogonal to my polar
        axis"""
        from isceobj.Util.geo.euclid import Vector
        if not isinstance(vector, Vector):
            try:
                vector = Vector(*vector)
            except Exception:
                raise ValueError(
                    "primary axis must a Vector or length 3 container"
                    )
            pass
        self._primary_axis = vector.hat()

        try:
            if self.polar_axis*self._primary_axis > 1.e-10:
                raise ValueError(
                    "polar_axis and primary_axis are not orthogonal"
                    )
        except AttributeError:
            class RaceHazard(Exception):
                """The outer class has methods that must be called in order.
                Should you fail to do so, this Exception shall be raised"""
                pass
            raise RuntimeError("You must set planet's polar axis first")
        
        self._ortho_axis = self.primary_axis.cross(self.polar_axis)
        pass
    pass

  

