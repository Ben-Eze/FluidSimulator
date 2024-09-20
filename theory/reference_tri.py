################################################################################
##
##  File: reference_tri.py
##
##  The MIT License
##
##  Copyright (c) 2006 Division of Applied Mathematics, Brown University (USA),
##  Department of Aeronautics, Imperial College London (UK), and Scientific
##  Computing and Imaging Institute, University of Utah (USA).
##
##  Permission is hereby granted, free of charge, to any person obtaining a
##  copy of this software and associated documentation files (the "Software"),
##  to deal in the Software without restriction, including without limitation
##  the rights to use, copy, modify, merge, publish, distribute, sublicense,
##  and/or sell copies of the Software, and to permit persons to whom the
##  Software is furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included
##  in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
##  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
##  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
##  DEALINGS IN THE SOFTWARE.
##
##  Description:  Calculate the time derivative of the scalar function X on a ##                reference triangular domain.
##                Since a single element is used with linear trial functions, ##                the second derivative (and thus diffusion) should be zero!
##
################################################################################

import numpy as np

def get_sigma_ij(ai, bi, gi, aj, bj, gj):
    # \sigma_{ij} = \int_{\Omega}\phi_i \phi_j d\Omega
    # the following is derived by integration
    return (
        ai*aj/2 + bi*bj/12 + gi*gj/12 + 
        (ai*bj + aj*bi)/6 + (ai*gj + aj*gi)/6 + (bi*gj + bj*gi)/24
    )

# Geometry
# a_i is the coordinate of the i'th vertex
a1 = np.array([0, 0])
a2 = np.array([1, 0])
a3 = np.array([0, 1])

rot_90cw = np.array([[ 0, 1],
                     [-1, 0]])

# N_{ij} is the unnormalised normal to the vector a_j - a_i
N12 = np.array(np.matmul(rot_90cw, (a2 - a1).T)).T
N23 = np.array(np.matmul(rot_90cw, (a3 - a2).T)).T
N31 = np.array(np.matmul(rot_90cw, (a1 - a3).T)).T
N = np.array([N12, N23, N31])

print(f"N12 = {N12}")
print(f"N23 = {N23}")
print(f"N31 = {N31}")

# Trial Functions
# \phi_i = \alpha_i + \beta_i x + \gamma_i y
# Alpha contains the trial function coefficients alpha, beta, gamma 
# ...for i = [1, 2, 3]
Alpha = np.array([[ 1, -1, -1],
                  [ 0,  1,  0],
                  [ 0,  0,  1]])

# Diffusive scalar field (X)
# A_i is the value of X at a_i
A = np.array([[1, 2, 3]])
print(f"A = {A}")

# \nabla X
gradX = np.matmul(A, Alpha[:, 1:])  # (1x2)
print(f"gradX = {gradX}")


# LHS = \int_{\Omega}\frac{\partial X}{\partial T} \phi_i d\Omega
#     = Sigma @ Adot
s11 = get_sigma_ij(*Alpha[0], *Alpha[0])
s12 = get_sigma_ij(*Alpha[0], *Alpha[1])
s13 = get_sigma_ij(*Alpha[0], *Alpha[2])
s22 = get_sigma_ij(*Alpha[1], *Alpha[1])
s23 = get_sigma_ij(*Alpha[1], *Alpha[2])
s33 = get_sigma_ij(*Alpha[2], *Alpha[2])

Sigma = np.array([[s11, s12, s13],
                  [s12, s22, s23],
                  [s13, s23, s33]])

print(f"Sigma = {Sigma}")

# R1 = \int_{\partial \Omega}(\phi_i \nabla X)\cdot \hat{n} ds
neighbouring_sides = np.array([[1, 0, 1],
                               [1, 1, 0],
                               [0, 1, 1]], dtype=float)

R1 = (0.5 * np.dot(gradX, np.matmul(neighbouring_sides, N).T)).T
print(f"R1 = {R1}")

# R2 = \int_{\Omega}\nabla \phi_i\nabla X d\Omega
R2 = 0.5 * np.matmul(Alpha[:, 1:], gradX.T)
assert((R2 == np.array([[2,-1,-1],[-1,1,0],[-1,0,1]]) @ A.T / 2).all())
print(f"R2 = {R2}")

# Whole equation
D = 1

# Sigma @ Adot = D(R1 - R2)
Adot = D * np.matmul(np.linalg.inv(Sigma), (R1 - R2))
print(f"Adot = {Adot}")

