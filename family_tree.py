class Person:

	def __init__(self, name):

		self.name = name

def add_parents(person):

	person.append([Person(raw_input('Mother of {}: '.format(person[0].name)))])
	person.append([Person(raw_input('Father of {}: '.format(person[0].name)))])


me = [Person(raw_input('What is your name? '))]

add_parents(me)

for i in me[1:]:
	add_parents(i)

for i in me[1:]:
	for x in i[1:]:
		add_parents(x)

print me