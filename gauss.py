
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
            print "Error: GaussBeam not properly initialzed. Can not print beam parameters"

class LensSystem( object ):
    def __init__(self, wavelength):
        self.wavelength=wavelength
        print "empty LensSystem created at wavelength of %.2f nm."%(wavelength / 1e-9)
        self.Lelements = []

    def MatrixMultiplication(self, A, B):
        result = [0,0,0,0]
        result[0] = A[0]*B[0] + A[1]*B[2]
        result[1] = A[0]*B[1] + A[1]*B[3]
        result[2] = A[2]*B[0] + A[3]*B[2]
        result[3] = A[2]*B[1] + A[3]*B[3]
        return result


    def add(self, Mtype, z, params):        
        if Mtype.lower()=="lens":
            newEle = {"z": z, "matrix": [1,0,-1./params[0],1],'type':'lens'}
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
            print "Bei z = %.3f das Element mit dem Index %d"%(zind[i][1],zind[i][0])

    def calculateQuntilZ(self,z_end):
        #get elements before z_end
        #find elements that are before z:
        zind = self.getListOrder()
        il = [ x for x in zind if x[1]<z_end]
        print "Anzahl elemente vorher:",len(il)
        for i in range(len(il)):
            print il[i]
            ### hier kommt jetzt die Berechnung der Gesamtmatrix hin


LS = LensSystem(633e-9)
LS.add('lens',.3,[1])
LS.add('lens',.1,[2])
LS.add('lens',4,[.2])
LS.add('lens',.2,[1.3])
LS.add('lens',.1,[1.3])
print LS.Lelements
print len(LS.Lelements)
#print LS.Lelements[]['z']

print LS.getListOrder()
LS.printPositions()


#print LS.MatrixMultiplication( [3,0,9,3],[5,10,7,0])

LS.calculateQuntilZ(0.5)

def gtest():
    g = GaussBeam(633e-9,"rw",[-12,0.1e-3])
    g2 = GaussBeam(633e-9,'q', -0.00020526 + -0.04962937j)
    g3 = GaussBeam(633e-9,'w', -0.00020526 + -0.04962937j)
    g.print_params()
    print ""
    g2.print_params()
    g3.print_params()

