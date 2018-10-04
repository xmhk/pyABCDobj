

# pyABCDobj ##
* rev 2 2014-03-10
* a object oriented framework to calculate the propagation of gaussian beams
* provides 2 Classes:
    * **GaussianBeam** - to calculate the beam parameters
    * **LensSystem**   - to calculate the propagation using the ABCD formalism

## class GaussianBeam ##
* **initialization**

    beam = **GaussianBeam( wavelength, mode, arg )**
    * wavelength is the wavelength in nm
    * mode is either 'q' or 'rw', which means you can define your beam by the complex beam parameters or a pair of  radius of curvature and waist (both given in meters)
    * examples:
        * b1 = GaussianBeam( 633e-9, 'q', 0 + .45j )
		* b2 = GaussianBeam( 1064-9, 'rw', [30, 2e-3])

* from the input parameters, the following physical values are calculated automatically:
    * **GaussianBeam.q** - the complex parameter q
    * **GaussianBeam.r** - the radius of curvature (phase)
    * **GaussianBeam.w** - the beam waist
    * **GaussianBeam.divergence** - the divergence in the far field
  
* furthermore, the beam wavelength is stored **GaussianBeam.wavelength**
* for convenience, all parameters can be printed out by **GaussianBeam.print\_params()**

---
## class LensSystem ##
### public methods
* **\_\_init\_\_(wavelength)**
    * initializes an empty lens system (wavelength in nm)


* **add_beam(mode, params)**:
    * adds a gaussian bean at z=0
    * **mode** is either 'rw' or 'q'

* **add_element( Type, zpos, params )**:
    * adds an element to the system.
    * **Type** can be
        * 'lens' (params = [focal length])
        * 'curvedmirror' (params = [Radius of curvature])
    * **zpos** is the z position of the element
    * **params** is a list of params (e.g. [f] for a simple lens)

* **calc_beam(zend,points)**:
    * calculates the beam up to **zend** with **points** as the number or points
    * returns  : [ w,r,d,z,q  ], where
        * **w** is the list of waists(z)
        * **r** is the list of beam curvatures
        * **d** is the list of divergences
        * **z** is the list of z values
        * **q** is the list of q values

* **calc\_propmatrix\_until\_z(z_end)**
    * calculates the propagation matrix up to z

* **clone()**
    * returns a copy of the lens system (without beams)

* **print_positions()**:
    * print positions of elements

### private methods
* **\_\_get\_list\_order** get the order of the elements in the lens system
* **\_\_matrix\_lens( f )** returns the ABCD matrix of a lens with focal length _f_
* **\_\_matrix\_free\_space( L, n)** returns the ABCD matrix of a free space propagation (length _L_, refractive index _n_) 

* **\_\_matrix\_curved\_mirror(self, R)** returns the ABCD matrix of a curved mirror with radius _R_
* **\_\_matrix\_multiplication( A, B )** perform matrix multiplication of _A_ and _B_




