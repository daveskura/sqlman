"""
  Dave Skura
  
"""
import logging
import sys

print (" Starting ") # 

class parser():
	def __init__(self,sqlfilename=''):
		self.join_tables = {}

		self.sqlfilename = sqlfilename
		f = open(self.sqlfilename,'r')
		self.sqlcontent = f.read()
		self.remove_comments()
		self.sqlines = self.sqlcontent.split('\n')
		self.sqlcontent = self.sqlcontent.replace('\n',' ')
		f.close()

		self.find_froms()
		self.find_joins()
		self.join_tables = sorted(self.join_tables)

	def remove_comments(self):
		newcontent = ''
		commenter = False
		linecommenter = False

		for i in range(0,len(self.sqlcontent)):
			if self.sqlcontent[i:i+2] == '/*':
				commenter = True
			
			if self.sqlcontent[i:i+2] == '--':
				linecommenter = True

			if self.sqlcontent[i] == '\n' and linecommenter:
				linecommenter = False

			if self.sqlcontent[i-2:i] == '*/':
				commenter = False

			if not commenter and not linecommenter:
				newcontent += self.sqlcontent[i]

		self.sqlcontent = newcontent

	def show(self):
		print(self.sqlcontent)

	def remove_in_clause(self,sql):
		newsql = ''
		in_started = False
		for i in range(0,len(sql)):
			if sql[i:i+2].upper() == 'IN':
				in_started = True

			if sql[i-1:i] == ')':
				in_started = False
			
			if not in_started:
				newsql += sql[i] 
		
		return newsql

	def find_froms(self):
		for line in self.sqlines:
			fromidx = line.upper().find('FROM')
			if fromidx > -1:
				fromline = line[fromidx+5:]
				fromtable = fromline.split(' ')[0].replace('`','')
				if fromtable != '(':
					fromtable = fromtable.replace(')','')
					self.join_tables[fromtable] = 'FROM'


	def find_joins(self):
		for line in self.sqlines:
			joinstart = line.upper().find('JOIN')
			if joinstart > -1:
				joinline = line[joinstart+5:]
				jointable = joinline.split(' ')[0].replace('`','')
				self.join_tables[jointable] = 'JOIN'

	def show_tables(self):
		for table in self.join_tables:
			print(table)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	logging.info(" Starting parser") # 

	p = parser('sample.sql')
	p.show_tables()
