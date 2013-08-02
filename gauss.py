
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

    def MatrixLens(self,f):
        return [1,0,-1.0/f,1]
    def MatrixFreeSpace(self, L,n):
        return [1,n*L,0,1]

    def MatrixMultiplication(self, A, B):
        result = [0,0,0,0]
        result[0] = A[0]*B[0] + A[1]*B[2]
        result[1] = A[0]*B[1] + A[1]*B[3]
        result[2] = A[2]*B[0] + A[3]*B[2]
        result[3] = A[2]*B[1] + A[3]*B[3]
        return result


    def add(self, Mtype, z, params):        
        if Mtype.lower()=="lens":
            newEle = {"z": z, "matrix": self.MatrixLens(params[0]),'type':'lens'}
            print "... appended a lens (f=%3f m) at z=%.3f m to the system"%(params[0],z)
            self.Lelements.append(newEle)
        else:
            print "unknown element :("

    def getListOrder(self):
        zind = sorted(enumerate([ele['z'] for ele in self.Lelements]),key=lambda x:x[1])
        return zind

    def printPositions(self):
        zind = self.getListOrder()
        for i in range(len(zind)):
            print "At z = %.3f is the element with number  %d"%(zind[i][1],zind[i][0])

    def calculatePropmatrixUntilZ(self,z_end):
        #get elements before z_end
        zind = self.getListOrder()
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
            M.append(self.MatrixFreeSpace(zdiff,1.0))
            M.append(self.Lelements[index]['matrix'])
        zdiff = z_end - aktz
        if self.verbose:
            print "after last element: %.4f m of air"%(zdiff)
        M.append(self.MatrixFreeSpace(zdiff,1.0))
        Mtot = [1,0,0,1]
        
        if self.verbose:
            print "Matrices including free space in reverse order:"
        for i in range(len(M)-1,-1,-1):
            Mtot = self.MatrixMultiplication(Mtot,M[i])
            if self.verbose:
                print M[i]
        if self.verbose:
            print "Total propagation matrix : ",Mtot
        return Mtot


    def addBeam(self, mode, params):
        self.beamZ0 = GaussBeam( self.wavelength, mode, params)


    def CalculateBeam( self, zend,points):
        dz = zend / 1.0 / points
        qlist = []
        zl = []
        for i in range(points):
            z = i * dz
            M = self.calculatePropmatrixUntilZ(z)
            qs = (self.beamZ0.q * M[0] + M[1]) /  (self.beamZ0.q * M[2] + M[3])
            qlist.append( GaussBeam( self.wavelength, 'q', qs))
            if self.verbose:
                qlist[i].print_params()
            zl.append(z)
        ws = [x.w for x in qlist]
        rs = [x.r for x in qlist]
        ds = [x.divergence for x in qlist]
#        z = [x*dz for x in range(points)]
        return ws,rs,ds,zl
            
            ## MTOT
            ## qdash

def gtest():
    g = GaussBeam(633e-9,"rw",[-12,0.1e-3])
    g2 = GaussBeam(633e-9,'q', -0.00020526 + -0.04962937j)
    g3 = GaussBeam(633e-9,'w', -0.00020526 + -0.04962937j)
    g.print_params()
    print ""
    g2.print_params()
    g3.print_params()


def LStest1():
    LS = LensSystem(633e-9)
    LS.add('lens',.3,[1])
    LS.add('lens',.1,[2])
    LS.add('lens',4,[.2])
    LS.add('lens',.2,[1.3])
    LS.add('lens',.1,[1.3])
    print LS.getListOrder()
    LS.printPositions()
    print LS.calculatePropmatrixUntilZ(.14)


from matplotlib import pyplot as plt

def LStest2():
    LS=LensSystem(633e-9)
    LS.add('lens',0.5,[0.09])

    LS.addBeam( 'rw',[-80,0.1e-3])
    ws,rs,ds,zs = LS.CalculateBeam(1.0, 2000)
    
    LS.beamZ0.print_params()
    plt.figure(1)
    plt.subplot(311)
    plt.plot(zs,ws)
    plt.subplot(312)
    plt.plot(zs,rs)
    plt.subplot(313)
    plt.plot(zs,ds)
    plt.savefig("lenstest2.pdf")
    plt.close(1)
LStest2()

