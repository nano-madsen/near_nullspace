import pytest
pytest.importorskip("fenics")

from fenics import *
from fenics_adjoint import *

from numpy.random import rand

mesh = UnitSquareMesh(2, 2)
cg2 = FiniteElement("CG", triangle, 2)
cg1 = FiniteElement("CG", triangle, 1)
ele = MixedElement([cg2, cg1])
Z = FunctionSpace(mesh, ele)
V2 = FunctionSpace(mesh, cg2)

def main(ic, fnsplit=True):
    u = Function(V2)
    w = TrialFunction(V2)
    v = TestFunction(V2)

    if fnsplit:
        ic_u = ic.split()[0]
    else:
        ic_u = split(ic)[0]

    mass = inner(w, v)*dx
    rhs  = inner(ic_u, v)*dx

    solve(mass == rhs, u)

    return u


def test_split():
    ic = Function(Z)

    u = main(ic, fnsplit=False)
    j = assemble(u**2*dx)
    rf = ReducedFunctional(j, Control(ic))

    taylor_test(rf, ic.copy(deepcopy=True), h=project(Constant([1, 1]), ic.function_space()))


def test_fn_split():
    set_working_tape(Tape())
    ic = Function(Z)

    u = main(ic, fnsplit=True)
    j = assemble(u**2*dx)
    rf = ReducedFunctional(j, Control(ic))

    h = Function(Z)
    h.vector()[:] = rand(Z.dim())
    taylor_test(rf, ic, h)
