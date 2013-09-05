
from gauss import *
from matplotlib import pyplot as plt

            

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
    LS.add_element('lens',.3,[1])
    LS.add_element('lens',.1,[2])
    LS.add_element('lens',4,[.2])
    LS.add_element('lens',.2,[1.3])
    LS.add_element('lens',.1,[1.3])
    print LS.get_list_order()
    LS.print_positions()
    print LS.calc_propmatrix_until_z(.14)


def LStest2():
    LS=LensSystem(633e-9)
    LS.add_element('lens',0.5,[0.09])

    LS.add_beam( 'rw',[-80,0.1e-3])
    ws,rs,ds,zs = LS.calc_beam(1.0, 2000)
    
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
