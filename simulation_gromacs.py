from openmm.app import *
from openmm import *
import openmm.unit
from sys import stdout

gro = GromacsGroFile(
    '/home/dhn/anaconda3/envs/openmm/share/openmm/examples/input.gro')
top = GromacsTopFile(
    '/home/dhn/anaconda3/envs/openmm/share/openmm/examples/input.top',
    periodicBoxVectors=gro.getPeriodicBoxVectors(),
    includeDir='/usr/local/gromacs/share/gromacs/top'
)
system = top.createSystem(
    nonbondedMethod=PME, nonbondedCutoff=1*unit.nanometer,
    constraints=HBonds
)
integrator = LangevinMiddleIntegrator(
    300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
simulation = Simulation(top.topology, system, integrator)
simulation.context.setPositions(gro.positions)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('output_gromacs.pdb', 1000))
simulation.reporters.append(StateDataReporter(
    stdout, 1000, step=True,
    potentialEnergy=True, temperature=True
))
simulation.step(10000)
