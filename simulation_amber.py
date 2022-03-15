from openmm.app import *
from openmm import *
import openmm.unit
from sys import stdout

prmtop = AmberPrmtopFile(
    '/home/dhn/anaconda3/envs/openmm/share/openmm/examples/input.prmtop')
inpcrd = AmberInpcrdFile(
    '/home/dhn/anaconda3/envs/openmm/share/openmm/examples/input.inpcrd')
system = prmtop.createSystem(
    nonbondedMethod=PME, nonbondedCutoff=1*unit.nanometer,
    constraints=HBonds
)
integrator = LangevinMiddleIntegrator(
    300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('output_amber.pdb', 1000))
simulation.reporters.append(StateDataReporter(
    stdout, 1000, step=True,
    potentialEnergy=True, temperature=True
))
simulation.step(10000)
