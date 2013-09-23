import Part
import math

#Variable
def bearing(params,document):
	R1 = 0.5*params['d1']
	R4 = 0.5*params['d2']
	#the inner two radii seem to be not specified in the standards, so we choose usefull values
	dr = (R4 - R1)/5.
	R2= R1 + 2*dr
	R3= R4 - 2*dr    #Variables. The main body of the bearing is created from 4 cylinders
	TH=params['B']    #Ball bearing thickness
	NBall=int(math.floor(math.pi*R1/dr))    #Ball number
	RBall=2*dr  #Ball radius
	RR=R4/40.        #Bearing edges rounding value
	name = params['name']

	shapes = []

	B1=Part.makeCylinder(R1,TH)
	B2=Part.makeCylinder(R2,TH)
	IR=B2.cut(B1)                             # Creates inner ring.
	FI=IR.Edges
	IR.makeFillet(RR,FI)

	B3=Part.makeCylinder(R3,TH)
	B4=Part.makeCylinder(R4,TH)
	OR=B4.cut(B3)                         #Creates outter ring
	FO=OR.Edges
	OR=OR.makeFillet(RR,FO)

	T1=Part.makeTorus(R2+(RBall/2),RBall)
	VT=(0,0,TH/2)
	T1.translate(VT)                      #Creates ball race

	IR=IR.cut(T1)
	OR=OR.cut(T1)

	shapes.append(IR)
	shapes.append(OR)

	CBall=((R3-R2)/2)+R2
	PBall=TH/2

	for i in range(NBall):                #Creates a number of NBalls
		Ball=Part.makeSphere(RBall)
		Alpha=(i*2*math.pi)/NBall 
		BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),TH/2)
		Ball.translate(BV)
		shapes.append(Ball)

	part = document.addObject("Part::Feature",name)
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()

bases = {'bearing' : bearing}