#!/usr/bin/env python2.7

import Tkinter as tk
import tkFileDialog	


class MainWindow(object):

	def __init__(self, parent):

		self.parent = parent
		
		self.PADX = 5
		
		self.REGFONT = ('Century Gothic',8, )
		self.TITLEFONT = ('Century Gothic',9, 'bold' )
		self.TITLEFONTBIG = ('Century Gothic',18, 'bold' )	

		self.BGCOLOR = 'white'

		self.newfamilyfile = True

		self.tree_frame = tk.Frame(self.parent)
		self.tree_frame.pack(side=tk.LEFT, padx=20)

		self.datascreen_frame = tk.Frame(self.parent)
		self.datascreen_frame.pack(side=tk.LEFT, padx=20)

		for i in [self.tree_frame, self.datascreen_frame, self.parent]:
			i.configure(bg=self.BGCOLOR)	

		self.make_string_vars()
		self.make_entry_controller()
		self.display_tree_diagram()		
		self.make_datascreen()
		self.make_menu()

	def make_menu(self):

		self.menubar = tk.Menu(root)

		self.filemenu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label='File', menu = self.filemenu)
		self.filemenu.add_command(label='Open', command=self.open_FAMILYfile)
		self.filemenu.add_command(label='Save', command=self.save_to_disk)
		self.filemenu.add_command(label='Save As', command=self.saveas_to_disk)

		self.helpmenu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label='Help', menu = self.helpmenu)
		self.helpmenu.add_command(label='Help', command=None)

	def make_string_vars(self):

		self.rel = tk.StringVar()
		
		self.name = tk.StringVar()
		self.fname = tk.StringVar()
		self.mname = tk.StringVar()
		self.lname = tk.StringVar()
		self.bname = tk.StringVar()
		self.dob = tk.StringVar()
		self.dod = tk.StringVar()
		self.pob = tk.StringVar()
		self.dom = tk.StringVar()
		#self.notes = tk.StringVar()
		
	def display_tree_diagram(self):
		
		# Manages layout of the Family Tree Diagram section
		
		# GENERATION HEADERS --
		titles = ['Individual', 'Parents', 'Grandparents', '     Great\ngrandparents', 
		' Great-great\ngrandparents', 'Great-great-great\n  grandparents']

		for i in xrange(6):

			self.gen_lbl = tk.Label(self.tree_frame, font=self.TITLEFONT, bg=self.BGCOLOR, text=titles[i], )
			self.gen_lbl.grid(row=0, column=i*2, pady=self.PADX)

		# GENERATION COLUMNS --
		
		# entry_controller is a list storing the Entry widgets in the tree 
		# diagram. (See self.make_entry_controller)
		e = self.entry_controller

		# Individual
		for i in e[0]:
			i['entry'].grid(row=31, column=0*2, rowspan=2, padx=self.PADX, ipady=0)

		# Parents
		for i in xrange(2):
			e[1][i]['entry'].grid(row=i*32+16, column=2, rowspan=2, padx=self.PADX)
			e[1][i]['entry'].configure(bg=self.get_gender_color(i))

		# Grandparents
		for i in xrange(4):
			e[2][i]['entry'].grid(row=i*16+8, column=4, rowspan=2, padx=self.PADX)
			e[2][i]['entry'].configure(bg=self.get_gender_color(i))

		# Great grandparents
		for i in xrange(8):
			e[3][i]['entry'].grid(row=i*8+4, column=6, rowspan=2, padx=self.PADX)
			e[3][i]['entry'].configure(bg=self.get_gender_color(i))

		# Great-great grandparents
		for i in xrange(16):
			e[4][i]['entry'].grid(row=i*4+2, column=8, rowspan=2, padx=self.PADX)
			e[4][i]['entry'].configure(bg=self.get_gender_color(i))

		# Great-great-great grandparents
		for i in xrange(32):
			e[5][i]['entry'].grid(row=i*2+1, column=10, rowspan=2, padx=5, pady=0)
			e[5][i]['entry'].configure(bg=self.get_gender_color(i))

	def get_gender_color(self, num):
		
		# returns blue for even number, pink for odd
		if num  % 2 == 0: return '#FFB6C1'
		else: return '#ADD8E6'

	def make_entry(self):

		# returns a tkinter Entry object
		entry = tk.Entry(self.tree_frame, font=self.REGFONT, width=22)
		entry.bind('<FocusIn>', self.get_fields)
		entry.bind('<KeyRelease>', self.save_title)
		entry.bind('<FocusOut>', self.save_fields)
		return entry

	def make_entry_controller(self):

		# creates the entry controller, a list of lists (each representing
		# a generation) of dictionaries (each representing an individual 
		# person). Dictionary key 'entry' holds a tk Entry object, and
		# key 'relation' holds a string code representing the person's
		# relationship to the root individual. 

		# 'i' = root/individual, 'm' = maternal, 'p' = paternal
		# e.g. 'immp' is the root's mother's mother's father

		# some recursive function fun to create the tree structure
		gens = [['i']]
		def add_gen(gen):

			if len(gen) < 17:
				
				parent_gen = []

				for i in gen:
					parent_gen.extend((i + 'm', i + 'p'))

				gens.append(parent_gen)
				add_gen(parent_gen)

		add_gen(gens[0])

		#for i in gens: print i

		self.entry_controller = []
		for gen in gens:
			self.entry_controller.append( [{'relation':i, 'entry':self.make_entry()} for i in gen] )

		#for i in self.entry_controller: print i
		
	def save_title(self, event):

		rel_code = self.get_relation_code(event)
		fam_data.datastruct[rel_code]['titlename'] = root.focus_get().get()
		self.name.set(fam_data.datastruct[rel_code]['titlename'])
		print self.name.get()

	def get_relation_code(self, event):

		# traverses entry_controller and returns relation code
		# corresponding to the Entry widget currently in focus
		for i in self.entry_controller:
			for x in i:
				if x['entry'] is root.focus_get():
					return x['relation']

	def get_fields(self, event):

		rel_code = self.get_relation_code(event)
		data = fam_data.datastruct[rel_code]
		
		self.rel.set(rel_code)		
		self.name.set(data['titlename'])
		self.fname.set(data['firstname'])
		self.mname.set(data['middlename'])
		self.lname.set(data['lastname'])
		self.bname.set(data['birthname'])
		self.dob.set(data['dateofbirth'])
		self.dod.set(data['dateofdeath'])
		self.pob.set(data['placeofbirth'])
		self.dom.set(data['dateofmarriage'])
		self.notes_text.delete(0.0, tk.END)
		print 'hey yo!'
		self.notes_text.insert(0.0, data['notes'])

		print self.fname

	def save_fields(self, event):


		print self.rel.get()
		data = fam_data.datastruct[self.rel.get()]

		data['titlename'] = self.name.get()
		data['firstname'] = self.fname.get()
		data['middlename'] = self.mname.get()
		data['lastname'] = self.lname.get()
		data['birthname'] = self.bname.get()
		data['dateofbirth'] = self.dob.get()
		data['dateofdeath'] = self.dod.get()
		data['placeofbirth'] = self.pob.get()
		data['dateofmarriage'] = self.dom.get()


		notes = self.notes_text.get(0.0, tk.END)
		print notes
		data['notes'] = notes

	def make_datascreen(self):

		self.name_lbl = tk.Label(self.datascreen_frame, font=self.TITLEFONTBIG, bg=self.BGCOLOR, textvariable=self.name)
		self.name_lbl.pack()

		self.datafields_frame = tk.Frame(self.datascreen_frame, bg=self.BGCOLOR,)
		self.datafields_frame.pack()
		
		fields = (

				('First Name', self.fname),
				('Middle Name: ', self.mname),
				('Last Name: ', self.lname),
				('Birth Name: ', self.bname),
				('Date of birth: ', self.dob),
				('Date of death: ', self.dod),
				('Place of birth: ', self.pob),
				('Marriage Date: ', self.dom),


				)



		for i in xrange(len(fields)):

			lbl = tk.Label(self.datafields_frame, font=self.TITLEFONT, bg=self.BGCOLOR, text=fields[i][0])
			lbl.grid(column=0, row=i)
			entry = tk.Entry(self.datafields_frame, font=self.REGFONT, bg=self.BGCOLOR, width=30, textvariable=fields[i][1])
			entry.grid(column=1, row=i, pady=3)
			entry.bind('<KeyRelease>', self.save_fields)

		lbl = tk.Label(self.datafields_frame, font=self.TITLEFONT, bg=self.BGCOLOR, text='Notes:            ')
		lbl.grid(column=0, row=len(fields))

		self.notes_text = tk.Text(self.datafields_frame, font=self.REGFONT, width=30, )
		self.notes_text.grid(column=1, row=len(fields), columnspan=1)
		self.notes_text.bind('<KeyRelease>', self.save_fields)



		# tk.Button(self.datascreen_frame, text='Save', command=self.saveas_to_disk).pack()
		# tk.Button(self.datascreen_frame, text='Open', command=self.open_FAMILYfile).pack()

	def save_to_disk(self):

		if self.newfamilyfile == True:			
			self.saveas_to_disk()
			self.newfamilyfile = False
			return
		else:
			x = str(fam_data.datastruct)
			with open(self.f, 'w') as fobj:
				fobj.write(x)

	def saveas_to_disk(self):
		
		x = str(fam_data.datastruct) 
		print x

		self.f = tkFileDialog.asksaveasfilename() 
		with open(self.f, 'w') as fobj:
			fobj.write(x)

	def open_FAMILYfile(self):

		self.f = tkFileDialog.askopenfilename()
		self.datafields_frame.destroy()
		self.make_datascreen()

		with open(self.f, 'rb') as fobj:
			x = eval(fobj.read())
			for k,v in x.iteritems(): 
				for gen in self.entry_controller:
					for n in gen:
						if n['relation'] == k:
							print n['relation'], k
							n['entry'].delete(0, tk.END)
							n['entry'].insert(0,v['titlename'])

			fam_data.datastruct = x

		new()

class FamilyData(object):

	def __init__(self):

		self.empty_family()

	def empty_family(self):

		self.datastruct = {'i':self.empty_person(),}

		def add_gen(rel):

			if len(rel) < 6:
				
				m = rel + 'm'
				p = rel + 'p'

				self.datastruct[m] = self.empty_person()
				self.datastruct[p] = self.empty_person()
				add_gen(m)
				add_gen(p)
		
		add_gen('i')

	def empty_person(self):

		null = ''

		return {


		'titlename': null,
		'firstname': null,
		'middlename': null,
		'lastname': null,
		'birthname': null,
		'dateofbirth': null,
		'dateofdeath': null,
		'placeofbirth': null,
		'notes': null,
		'dateofmarriage': null,


		}


	def print_datastruct(self):
		for key, value in self.datastruct.iteritems(): print key, value


def new():
	del(app)
	del(fam_data)
	app = MainWindow(root)
	fam_data = FamilyData()






fam_data = FamilyData()

root = tk.Tk()
app = MainWindow(root)
root.state('zoomed')
root.title('Family Tree')

root.config(menu=app.menubar)
root.mainloop()




























