import numpy as np
from scipy.optimize import fsolve
import math
from numpy import exp
import timeit
from random import random



def myFunction(vars):
    (a,b,c,d) = vars
    epsilon, phi_curl, _, theta = getVars()

    first_eq = epsilon[0] + phi_curl * (a * theta[0,0] + b * theta[0,1] + c * theta[0,2] + d * theta[0,3]) - a
    second_eq = epsilon[1] + phi_curl * (a * theta[1,0] + b * theta[1,1] + c * theta[1,2] + d * theta[1,3]) - b
    third_eq = epsilon[2] + phi_curl * (a * theta[2,0] + b * theta[2,1] + c * theta[2,2] + d * theta[2,3]) - c
    fourth_eq = epsilon[3] + phi_curl * (a * theta[3,0] + b * theta[3,1] + c * theta[3,2] + d * theta[3,3]) - d
    return [first_eq, second_eq, third_eq, fourth_eq]


def linearSolution():
    st1 = timeit.default_timer()
    solution = fsolve(myFunction, (0.1,0.1,0.1,0.1))
    st2 = timeit.default_timer()
    # print(solution)
    # print("RUN TIME : {0}".format(st2-st1))
    return solution

def convergence(linear_solution):
    start_vector = linear_solution
    epsilon, phi_curl, phi_str, theta = getVars()
    
    converged = False
    end_vector = start_vector

    while not converged:
        a,b,c,d = end_vector
        first_e = epsilon[0] + phi_curl * ((a * theta[0,0])**phi_str + 
            (b * theta[0,1])**phi_str + (c * theta[0,2])**phi_str + (d * theta[0,3])**phi_str)
        second_e = epsilon[1] + phi_curl * ((a * theta[1,0])**phi_str + 
            (b * theta[1,1])**phi_str + (c * theta[1,2])**phi_str + (d * theta[1,3])**phi_str)
        third_e = epsilon[2] + phi_curl * ((a * theta[2,0])**phi_str + 
            (b * theta[2,1])**phi_str + (c * theta[2,2])**phi_str + (d * theta[2,3])**phi_str)
        fourth_e = epsilon[3] + phi_curl * ((a * theta[3,0])**phi_str + 
            (b * theta[3,1])**phi_str + (c * theta[3,2])**phi_str + (d * theta[3,3])**phi_str)
        end_vector = [first_e, second_e, third_e, fourth_e]

        converged = checkConvergence(start_vector, end_vector)


def checkConvergence(start_vector, end_vector):
    sum = 0
    for start, end in zip(start_vector, end_vector):
        print(abs(start-end))
        sum += abs(start-end)

    if sum <= 0.001:
        return True
    else:
        return False


def getVars():
    epsilon = np.array([0.30054265, 0.07424462, 0.09276756, 0.44549839])
    phi_curl = 0.2
    phi_str = 1
    theta = np.array([
        [0.5275144901251466, 0.29852084466689666, 0.6191157837454203, 0.23833707775302404],
        [0.4554009654456119, 0.2636690520105859, 0.6809365408206707, 0.7275647260322592],
        [0.4065147070897367, 0.3071596453854798, 0.5287791570802208, 0.18249395994037187],
        [0.23185232556707946, 0.28919106338907585, 0.3557328342748909, 0.21527485086098863],
    ])
    return epsilon, phi_curl, phi_str, theta

def main():
    linear_solution = linearSolution()
    E_star = convergence(linear_solution)
    

if __name__ == "__main__":
    main()

