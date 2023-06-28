

class Species:
	'''
	'''
	def __init__(self, l):
		if len(l) == 3:
			self.hasIndex = True
			self.phi = float(l[1])
			self.mu = float(l[2])
		else:
			self.hasIndex = False
			self.phi = float(l[0])
			self.mu = float(l[1])

class Thermo:
	'''
	'''
	def __init__(self, filename=None):
		self.fHelmholtz = None
		self.pressure = None
		self.fIdeal = None
		self.fInter = None
		self.fExt = None
		self.Polymers = None
		self.Solvents = None
		self.LatticeParameters = None
		self.tableLable = None

		if filename != None:
			with open(filename) as f:
				self.read(f)

	def read(self, openFile):
		line = self.skipEmptyLine(openFile)
		l = line.split()
		if l[0] != 'fHelmholtz':
			raise Exception('Not valid Thermo file')
		else:
			self.fHelmholtz = float(l[1])
		line = openFile.readline()
		l = line.split()
		self.pressure = float(l[1])
		line = self.skipEmptyLine(openFile)

		while line != '\n':
			if line == 'Free energy components:\n':
				line = openFile.readline()
				while line != '\n':
					l = line.split()
					if l[0] == 'fIdeal':
						self.fIdeal = float(l[1])
					if l[0] == 'fInter':
						self.fInter = float(l[1])
					if l[0] == 'fExt':
						self.fExt = float(l[1])
					line = openFile.readline()

			if line == 'Polymers:\n':
				self.Polymers = []
				self.tableLable = openFile.readline()
				line = openFile.readline()
				while line != '\n':
					l = line.split()
					self.Polymers.append(Species(l))
					line = openFile.readline()

			if line == 'Solvents:\n':
				self.Solvents = []
				line = openFile.readline()
				line = openFile.readline()
				while line != '\n':
					l = line.split()
					self.Solvents.append(Species(l))
					line = openFile.readline()

			if line == 'Lattice parameters:\n':
				self.LatticeParameters = []
				line = openFile.readline()
				l = line.split()
				for i in range(len(l)):
					self.LatticeParameters.append(float(l[i]))

			line = self.skipEmptyLine(openFile)

			if line == '':
				break

	def skipEmptyLine(self, openFile):
		line = openFile.readline()
		while line == '\n':
			line = openFile.readline()
		return line

	def writeOut(self, filename):
		with open(filename, 'w') as f:
			f.write(self.writeOutString())

	def writeOutString(self):
		s = ''
		s += 'fHelmholtz'
		v = f'{self.fHelmholtz:.11e}'
		s += f'{v:>22}\n'
		s += 'pressure  '
		v = f'{self.pressure:.11e}'
		s += f'{v:>22}\n'
		s += '\n'

		if (self.fIdeal != None) or (self.fInter != None) or (self.fExt != None):
			s += 'Free energy components:\n'
			if self.fIdeal != None:
				s += 'fIdeal    '
				v = f'{self.fIdeal:.11e}'
				s += f'{v:>22}\n'
			if self.fInter != None:
				s += 'fInter    '
				v = f'{self.fInter:.11e}'
				s += f'{v:>22}\n'
			if self.fExt != None:
				s += 'fExt      '
				v = f'{self.fExt:.11e}'
				s += f'{v:>22}\n'
			s += '\n'

		s += 'Polymers:\n'
		s += self.tableLable
		if self.Polymers[0].hasIndex == True:
			for i in range(len(self.Polymers)):
				p = f'{self.Polymers[i].phi:.11e}'
				m = f'{self.Polymers[i].mu:.11e}'
				s += f'{i:>5}{p:>20}{m:>20}\n'
		else:
			for i in range(len(self.Polymers)):
				p = f'{self.Polymers[i].phi:.11e}'
				m = f'{self.Polymers[i].mu:.11e}'
				s += f'     {p:>20}{m:>20}\n'
		s += '\n'

		if self.Solvents != None:
			s += 'Solvents:\n'
			s += self.tableLable
			if self.Solvents[0].hasIndex == True:
				for i in range(len(self.Polymers)):
					p = f'{self.Solvents[i].phi:.11e}'
					m = f'{self.Solvents[i].mu:.11e}'
					s += f'{i:>5}{p:>20}{m:>20}\n'
			else:
				for i in range(len(self.Polymers)):
					p = f'{self.Solvents[i].phi:.11e}'
					m = f'{self.Solvents[i].mu:.11e}'
					s += f'     {p:>20}{m:>20}\n'
			s += '\n'

		if self.LatticeParameters != None:
			s += 'Lattice parameters:\n'
			s += '       '
			v = f'{self.LatticeParameters[0]:.11e}'
			s += f'{v:>18}'
			if len(self.LatticeParameters) > 1:
				for i in range(1, len(self.LatticeParameters)):
					v = f'{self.LatticeParameters[i]:.11e}'
					s += f'{v:>20}'
			s += '\n'

		s += '\n'

		return s

t = Thermo('dat')
# print(f'{t.fHelmholtz:.11e}')
t.writeOut('datOut')

t2 = Thermo('thermo')
t2.writeOut('thermoOut')










