import requests,json;	
import pickle;
import sys;

class Lookup:
	""" class used to query the NHTSA Database as well as read stored .car files """

	def printValues(self, car):
		""" takes a Car object and prints values without a blank field as well as make, model, and VIN """
		print(car.make, "-", car.model)
		print("VIN#", car.VIN)
		print("-"*30)

		for i in car.values["Results"]:
			if i["Value"]:
				print(i["Variable"], ":", i["Value"])

	def searchMakeAndModel(self, VIN):
		""" takes a VIN number and uses the NHTSA API to lookup information about the vehicle and store it """
		url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/%s*BA?format=json' % VIN
		try:
			r = requests.get(url)
		except:
			print("Error: VIN not found!")
			return
		# adapted from https://vpic.nhtsa.dot.gov/api/Home/Index/LanguageExamples

		reformatted = json.loads(r.text)

		car = Car()

		car.values = reformatted
		car.findInfo()

		self.printValues(car)

		return car;

	def loadMakeAndModel(self, file):
		""" takes a filename (ending in .car) and extracts and stores the data in a Car object """
		car = Car()
		car.unpickleCar(file)
		car.findInfo()

		self.printValues(car)

		return car

class Car:
	""" class used to store information about cars """
	make = ""
	model = ""
	VIN = ""
	values = {}

	def findInfo(self):
		""" assigns values to make, model, and VIN using the values variable """
		self.make = self.values["Results"][5]["Value"]
		self.model = self.values["Results"][7]["Value"]

		self.VIN = self.values["SearchCriteria"][4:]

	def pickleCar(self):
		""" saves car data to file named make-model.car (ex: ford-pinto.car)"""
		# create .car file
		try:
			pickle.dump(self.values, open("%s-%s.car" % (self.make.lower(), self.model.lower().replace(" ", "_")), "wb"))
		except:
			sys.exit("Error: Unable to pickle object!")

	def unpickleCar(self, filename):
		""" loads .car file and stores it """
		try:
			self.values = pickle.load(open(filename, "rb"))
		except:
			sys.exit("Error: Unable to load file!")

def main():
	""" main function """
	lookup = Lookup()

	try:
		argument = sys.argv[1]

	except:
		print("Error: not enough arguments!")
		return

	#determine if file or query
	if ".car" in argument:
		#load
		lookup.loadMakeAndModel(argument)
	else:
		#query
		try:
			car = lookup.searchMakeAndModel(argument)
		except:
			print("Error: Unable to query VIN!")
			return
		car.pickleCar()

if __name__ == "__main__":
	main()