import numpy
import csv
import os
import time

newcluster = 0
Papers = []
Clusters = []
TrueClusters = {}
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

def DelCluster(cluster1):
	for i,c in enumerate(Clusters):
		if(Clusters[i]==cluster1):
			del(Clusters[i])
			break

	return 
def CombineCluster(cluster1,cluster2):


	global newcluster
	tmp = Cluster(newcluster)
	newcluster+=1


	for i in cluster1.papers:
		tmp.add(i)

	for i in cluster2.papers:
		tmp.add(i)

	return tmp
def CombineMergelist(mergelist):
	for line in mergelist:

		tmp = line[0]
	for c in range(1,len(line)):
		tmp = CombineCluster(tmp,line[c])

	Clusters.append(tmp)

	for i in line:
		DelCluster(i)


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
		if(coauthors[0]==''):
			coauthors = []
		label = line[1] 
		author = line[2]




		Papers.append(Paper(ID,title,year,venue_id,affiliation_id,coauthors,label,author))

def Common_coauthor():
	void_repeat = set()

	mergelist = []
	tail = 0

	for i in range(len(Clusters)):
		for j in range(i+1,len(Clusters)):
			
			
			

			papers1 = Clusters[i].papers
			papers2 = Clusters[j].papers

			flag = False

			for paper1 in papers1:
				for paper2 in papers2:

					if(paper1.affiliation_id==paper2.affiliation_id):

						flag= True
						break
					if(flag):
						break
				if(flag):
					break


			if(flag):
				flag = False

				for k in range(tail):
					if(Clusters[i] in mergelist[k]):
						flag=True

						if(Clusters[j] not in mergelist[k]):
							mergelist[k].append(Clusters[j])
						break
					if(Clusters[j] in mergelist[k]):
						flag=True

						if(Clusters[i] not in mergelist[k]):
							mergelist[k].append(Clusters[i])
						break

				if(flag==False):
					mergelist.append([])
					mergelist[tail].append(Clusters[i])
					mergelist[tail].append(Clusters[j])
					tail+=1
	
	return mergelist





def Common_affiliation():
	mergelist = []
	tail = 0

	for i in range(len(Clusters)):
		for j in range(i+1,len(Clusters)):
			
			
			

			papers1 = Clusters[i].papers
			papers2 = Clusters[j].papers

			flag = False

			for paper1 in papers1:
				for paper2 in papers2:

					for co1 in paper1.coauthors:
						for co2 in paper2.coauthors:
							if(co1 == co2):
	
								flag= True
								break
					if(flag):
						break
				if(flag):
					break


			if(flag):
				flag = False

				for k in range(tail):
					if(Clusters[i] in mergelist[k]):
						flag=True

						if(Clusters[j] not in mergelist[k]):
							mergelist[k].append(Clusters[j])
						break
					if(Clusters[j] in mergelist[k]):
						flag=True

						if(Clusters[i] not in mergelist[k]):
							mergelist[k].append(Clusters[i])
						break

				if(flag==False):
					mergelist.append([])
					mergelist[tail].append(Clusters[i])
					mergelist[tail].append(Clusters[j])
					tail+=1
	
	return mergelist

def CalculateMetrix(Clusters):

	a = 0
	for i in range(len(Papers)):
		for j in range(i+1,len(Papers)):
			if(Papers[i].label == Papers[j].label):
				#print (i,type(Papers[i].label_predicted))
				#print (j,type(Papers[j].label_predicted))
				if(Papers[i].label_predicted == Papers[j].label_predicted):
					a+=1

	ac = 0
	ab = 0

	for c in Clusters:
		ac+=len(c.papers)*(len(c.papers)-1)/2

	for c in TrueClusters:
		ab+=len(TrueClusters[c])*(len(TrueClusters[c])-1)/2

	pp = float(a)/float(ac)
	pr = float(a)/float(ab)


	print ("PF1 metrix is ",2*pp*pr/(pp+pr))


if __name__ == '__main__':




	file_name = "BobJohnson.txt"
	read_file(file_name)


	for paper in Papers:
		tmp = Cluster(newcluster)
		tmp.add(paper)

		Clusters.append(tmp)  

		if(paper.label not in TrueClusters):
			TrueClusters[paper.label]=[]
		TrueClusters[paper.label].append(paper)

		newcluster+=1 

	#Clusters.append(CombineCluster(Clusters[1],Clusters[0]))
	#DelCluster(Clusters[1])
	#DelCluster(Clusters[0])



	mergelist = Common_coauthor()
	CombineMergelist(mergelist)


	mergelist = Common_affiliation()
	CombineMergelist(mergelist)



	Statement()

	CalculateMetrix(Clusters)






