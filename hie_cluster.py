import numpy
import csv
import os
import time

newcluster = 0
Papers = []
Clusters = []

class Paper:
	def __init__(self, ID, title, year, venue_id, affiliation_id, coauthors, label, author):
		self.ID = ID
		self.title = title
		self.year = year
		self.venue_id = venue_id
		self.affiliation_id = affiliation_id
		self.coauthors = coauthors
		self.label = label
		self.label_predicted = 0
		self.author = author
	def speak(self):
		print ("paper_id:",self.ID)
		print ("title:",self.title)
		print ("year:",self.year)
		print ("venue_id:",self.venue_id)
		print ("affiliation:",self.affiliation_id)
		print ("coauthors:",self.coauthors)
		print ("label:",self.label)
		print ("label_predicted:",self.label_predicted)
		print ("author:",self.author)

	def speakshort(self):
		print ("paper_id:",self.ID," label:",self.label," label_predicted:",self.label_predicted)

class Cluster:
	def __init__(self, label):
		self.papers = []
		self.label = label

	def add(self,paper):
		self.papers.append(paper)
		paper.label_predicted = self.label
	def speak(self):
		print ("Cluster label:",self.label," Paper num:",len(self.papers))
		for i in self.papers:
			i.speakshort()

def CombineCluster(cluster1,cluster2):
	for i,c in enumerate(Clusters):
		if(Clusters[i]==cluster1):
			del(Clusters[i])
			break

	for i,c in enumerate(Clusters):
		if(Clusters[i]==cluster2):
			del(Clusters[i])
			break

	global newcluster
	tmp = Cluster(newcluster)
	newcluster+=1


	for i in cluster1.papers:
		tmp.add(i)

	for i in cluster2.papers:
		tmp.add(i)

	Clusters.append(tmp)

def Statement():

	for i in Clusters:
		print ("----------------")
		i.speak()
		print ("----------------")

def read_file(file_name):
	ret = open(file_name).readlines()

	for line in ret:
		line = line.split(";")
		#11;5;j yin;andrzej s kozek;on gauss quadrature and partial cross validation;affiliation;venue;2004
		ID = line [0]
		title = line[4]
		year = line[7]
		venue_id = line[6]
		affiliation_id = line[5]
		coauthors = line[3].split(",")
		label = line[1] 
		author = line[2]




		Papers.append(Paper(ID,title,year,venue_id,affiliation_id,coauthors,label,author))

def Common_coauthor():
	void_repeat = set()
	for i in range(len(Clusters)):
		for j in range(i+1,len(Clusters)):
			
			
			if(str(cluster1.label)+"-"+str(cluster2.label) not in void_repeat):
				void_repeat.add(str(cluster1.label)+"-"+str(cluster2.label))
				void_repeat.add(str(cluster2.label)+"-"+str(cluster1.label))
			else :
				continue

			papers1 = cluster1.papers
			papers2 = cluster2.papers

			 


def Common_affiliation():

	return

if __name__ == '__main__':




	file_name = "BobJohnson.txt"
	read_file(file_name)


	for paper in Papers:
		tmp = Cluster(newcluster)
		tmp.add(paper)

		Clusters.append(tmp)  

		newcluster+=1 
	Statement()

	print ("over!!!!!!!!!!!!!!!!!!")
	CombineCluster(Clusters[1],Clusters[0])
	Statement()


	#Common_coauthor()
	#Common_affiation()







