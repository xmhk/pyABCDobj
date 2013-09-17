## pyABCDobj ##
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


## pyABCDobj ##