#
# Textbook example: Rabi oscillations in a driven two-level system. This
# example show how to solve a problem with a arbitrarily time-dependent
# Hamiltonian. 
#
from qutip import *
from pylab import *
import time

def hamiltonian_t(t, args):
    #
    # evaluate the hamiltonian at time t. 
    #
    H0 = args[0]
    H1 = args[1]
    w  = args[2]

    return H0 + H1 * sin(w * t)

def sd_qubit_integrate(delta, eps0, A, w, gamma1, gamma2, psi0, tlist):

    # Hamiltonian
    sx = sigmax()
    sz = sigmaz()
    sm = destroy(2)

    H0 = - delta/2.0 * sx - eps0/2.0 * sz
    H1 = - A * sx
        
    H_args = (H0, H1, w)

    # collapse operators
    c_op_list = []

    n_th = 0.0 # zero temperature

    # relaxation
    rate = gamma1 * (1 + n_th)
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * sm)

    # excitation
    rate = gamma1 * n_th
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * sm.dag())

    # dephasing 
    rate = gamma2
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * sz)


    # evolve and calculate expectation values
    expt_list = odesolve(hamiltonian_t, psi0, tlist, c_op_list, [sm.dag() * sm], H_args)  

    return expt_list[0]
    
#
# set up the calculation
#
delta = 0.0  * 2 * pi   # qubit sigma_x coefficient
eps0  = 1.0  * 2 * pi   # qubit sigma_z coefficient
A     = 0.05 * 2 * pi   # driving amplitude (sigma_x coupled)
w     = 1.0  * 2 * pi   # driving frequency

gamma1 = 0.025          # relaxation rate
gamma2 = 0.0            # dephasing  rate

# intial state
psi0 = basis(2,0)

tlist = linspace(0,50,500)

start_time = time.time()
p_ex = sd_qubit_integrate(delta, eps0, A, w, gamma1, gamma2, psi0, tlist)
print 'time elapsed = ' + str(time.time() - start_time) 

plot(tlist, real(p_ex))
xlabel('Time')
ylabel('P_ex')
title('Excitation probabilty of qubit')
#savefig("qubit_rabi.png")
show()


