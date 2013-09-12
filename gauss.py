
CONST_PI=3.14159265359

class GaussBeam(object):
    initsuccess = False
    def __init__(self, wavelength, mode, arg):
        self.wavelength = wavelength
        if mode.lower() == "q":
            self.q = arg
            self.r = abs(self.q)**2 / self.q.real 
            self.w = abs(self.wavelength / CONST_PI * abs(self.q)**2  / self.q.imag)**0.5
            self.divergence = ( self.wavelength/CONST_PI / abs( self.q.imag )) ** 0.5
            self.initsuccess = True
        elif mode.lower() =="rw":
            self.r = arg[0]
            self.w = arg[1]
            self.q = 1.0 / ( 1.0/self.r  + 1.0j * self.wavelength / (CONST_PI * self.w**2))
            self.divergence = ( self.wavelength/CONST_PI / abs( self.q.imag )) ** 0.5
            self.initsuccess = True
        else:
            print "Please use GaussBeam('q', wavelength, qVal) or GaussBeam('rw',wavelength, [R,w])"

    def print_params(self):
        if self.initsuccess:
            print "q    = %.8f + %.8fj"%(self.q.real,self.q.imag)
            print "w    = %.5f mm"%(self.w / 1e-3)
            print "R    = %.5f m "%self.r
            print "div  = %.5f mrad (divergence far field)"%(self.divergence/1e-3) 
        else:
            print "Error: GaussBeam not properly initialzed. Can not print beam"

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class LensSystem( object ):
    verbose = False
    def __init__(self, wavelength):
        self.wavelength=wavelength
        print "empty LensSystem created at wavelength of %.2f nm."%(wavelength / 1e-9)
        self.Lelements = []
    def clone(self):
        LSclone = LensSystem(self.wavelength)
        LSclone.Lelements = self.Lelements
        return LSclone

    def matrix_lens(self,f):
        return [1,0,-1.0/f,1]

    def matrix_free_space(self, L,n):
        return [1,n*L,0,1]

    def matrix_curved_mirror(self, R):
        return [1.0,0.0,  -2.0/R,1.0]

    def __matrix_multiplication(self, A, B):
        result = [0,0,0,0]
        result[0] = A[0]*B[0] + A[1]*B[2]
        result[1] = A[0]*B[1] + A[1]*B[3]
        result[2] = A[2]*B[0] + A[3]*B[2]
        result[3] = A[2]*B[1] + A[3]*B[3]
        return result

    def add_element(self, Mtype, z, params):        
        if Mtype.lower()=="lens":
            newEle = {"z": z, "matrix": self.matrix_lens(params[0]),'type':'lens'}
            print "... appended a lens (f=%.5f m) at z=%.5f m to the system"%(params[0],z)
            self.Lelements.append(newEle)
        else:
            print "unknown element :("

    def get_list_order(self):
        zind = sorted(enumerate([ele['z'] for ele in self.Lelements]),key=lambda x:x[1])
        return zind

    def print_positions(self):
        zind = self.get_list_order()
        for i in range(len(zind)):
            print "At z = %.3f is the element with number  %d"%(zind[i][1],zind[i][0])

    def calc_propmatrix_until_z(self,z_end):
        #get elements before z_end
        zind = self.get_list_order()
        #find elements that are before z:
        ElementList = [ x for x in zind if x[1]<z_end]
        M = []
        aktz = 0
        if self.verbose:
            print "Z_end = ",z_end
            print "number of elements before: ",len(ElementList)
        for i in range(len(ElementList)):
            zwert = ElementList[i][1]
            index = ElementList[i][0]
            zdiff = zwert-aktz
            aktz = zwert
            if self.verbose:
                print "air: %.4f m, then element number %d"%(zdiff,index)
            M.append(self.matrix_free_space(zdiff,1.0))
            M.append(self.Lelements[index]['matrix'])
        zdiff = z_end - aktz
        if self.verbose:
            print "after last element: %.4f m of air"%(zdiff)
        M.append(self.matrix_free_space(zdiff,1.0))
        Mtot = [1,0,0,1]
       
        if self.verbose:
            print "Matrices including free space in reverse order:"
        for i in range(len(M)-1,-1,-1):
            Mtot = self.__matrix_multiplication(Mtot,M[i])
            if self.verbose:
                print M[i]
        if self.verbose:
            print "Total propagation matrix : ",Mtot
        return Mtot


    def add_beam(self, mode, params):
        self.beamZ0 = GaussBeam( self.wavelength, mode, params)


    def calc_beam( self, zend,points):
        dz = zend / 1.0 / points
        qlist = []
        zl = []
        for i in range(points):
            z = i * dz
            M = self.calc_propmatrix_until_z(z)
            qs = (self.beamZ0.q * M[0] + M[1]) /  (self.beamZ0.q * M[2] + M[3])
            qlist.append( GaussBeam( self.wavelength, 'q', qs))
            if self.verbose:
                qlist[i].print_params()
            zl.append(z)
        ws = [x.w for x in qlist]
        rs = [x.r for x in qlist]
        ds = [x.divergence for x in qlist]
#        z = [x*dz for x in range(points)]
        return ws,rs,ds,zl,[x.q for x in qlist]


