from openmm.app import *
from openmm import *
import openmm.unit
from sys import stdout

print(unit.nanometer)

pdb = PDBFile(
    '/home/dhn/anaconda3/envs/openmm/share/openmm/examples/input.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
system = forcefield.createSystem(
    pdb.topology, nonbondedMethod=PME,
    nonbondedCutoff=1*unit.nanometer, constraints=HBonds
)
integrator = LangevinMiddleIntegrator(
    300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('output_test.pdb', 1000))
simulation.reporters.append(StateDataReporter(
    stdout, 1000, step=True,
    potentialEnergy=True, temperature=True
))
simulation.step(10000)
