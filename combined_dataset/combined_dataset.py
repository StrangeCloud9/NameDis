# coding:utf-8
import os
from lxml import html
import re
import pymysql as MySQLdb
import random 

conn = MySQLdb.connect(host='202.120.36.29', port=6033, user='groupleader', passwd='onlyleaders', db='mag-new-160205',
                       charset="utf8")
cursor = conn.cursor()

class Paper:
    def __init__(self, paper_id, title, year, venue_id, affiliation_id, coauthors, label, author):
        self.paper_id = paper_id
        self.title = title
        self.year = year
        self.venue_id = venue_id
        self.affiliation_id = affiliation_id
        self.coauthors = coauthors
        self.label = label
        self.label_predicted = 0
        self.author = author


def get_file_list(dir, file_list):
    newDir = dir
    if os.path.isfile(dir):
        file_list.append(dir.decode('gbk'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            get_file_list(newDir, file_list)
    return file_list



def generate_paper_instance_list(file):
    author_name = file.split('\\')[-1].replace('.xml', '')
    author_name = author_name.lower()
    author_name = re.sub('[^A-Za-z0-9]', ' ', author_name)
    author_name = re.sub('\s{2,}', ' ', author_name)

    tree = html.parse(file)
    root = tree.getroot()

    paper_instance_list = list()

    for node in root.xpath('//publication'):
        label = node.xpath('label')[0].text
        title = node.xpath('title')[0].text

        title = title.lower()

        if title[-1] == '.':
            title = title[:-1]
        title = re.sub('[^A-Za-z0-9]', ' ', title)
        title = re.sub('\s{2,}', ' ', title)
        quest_paper_by_title = 'SELECT PaperID FROM Papers WHERE NormalizedPaperTitle="%s"'
        cursor.execute(quest_paper_by_title % title)
        ps = cursor.fetchall()

        paper_ids = list()
        if len(ps) == 1:
            paper_ids.append(ps[0][0])
        if len(ps) >= 2:
            for p in ps:
                quest_author_by_paper = 'SELECT AuthorName FROM Authors INNER JOIN' \
                                        '	(SELECT AuthorID FROM PaperAuthorAffiliations AS PAA  WHERE PaperID="%s") AS TB2' \
                                        '	ON Authors.AuthorID = TB2.AuthorID'
                cursor.execute(quest_author_by_paper % p[0])
                authors = cursor.fetchall()
                for author in authors:
                    if author[0] == author_name.lower():
                        paper_ids.append(p[0])


        for paper_id in paper_ids:

            # get affiliation and coauthors
            quest_affiliation = 'SELECT AuthorName,AffiliationID FROM Authors INNER JOIN' \
                                '	(SELECT AuthorID,AffiliationID FROM PaperAuthorAffiliations WHERE PaperID="%s") AS TB ' \
                                'ON Authors.AuthorID = TB.AuthorID'
            cursor.execute(quest_affiliation % paper_id)
            author_affiliations = cursor.fetchall()

            himself = None
            for ai in range(len(author_affiliations)):
                if author_affiliations[ai][0] == author_name.lower():
                    himself = ai
                    break

            if himself is None:
                tmp1 = author_name.split()
                for ai in range(len(author_affiliations)):
                    tmp2 = author_affiliations[ai][0].split()
                    if tmp1[-1] == tmp2[-1] and tmp1[0][0] == tmp2[0][0]:
                        himself = ai
                        break
                    elif tmp1[-1] == tmp2[0] and tmp1[0][0] == tmp2[-1][0]:
                        himself = ai
                        break

            # get affiliation
            if himself is None:
                affiliation_id = author_affiliations[-1][1]
            else:
                affiliation_id = author_affiliations[himself][1]


            # get coauthors
            coauthors = set()
            for ai in range(len(author_affiliations)):
                if ai != himself:
                    coauthor_name = author_affiliations[ai][0]
                    coauthors.add(coauthor_name)

            # get venue, title and year
            venue_id = None
            year = None
            quest_info_by_paper = 'SELECT NormalizedPaperTitle, ConferenceSeriesIDMappedToVenueName, ' \
                                  'JournalIDMappedToVenueName, PaperPublishYear FROM Papers WHERE PaperID = "%s"'
            cursor.execute(quest_info_by_paper % paper_id)
            rs = cursor.fetchall()
            if len(rs) != 0:
                # fill in paper_venue_dict
                if rs[0][1] is not None:
                    venue_id = rs[0][1]
                elif rs[0][2] is not None:
                    venue_id = rs[0][2]

                year = rs[0][3]

            paper_instance = Paper(paper_id, title, year, venue_id, affiliation_id, coauthors, label, author_name)
            paper_instance_list.append(paper_instance)

    return paper_instance_list


if __name__ == '__main__':
    file_list = get_file_list('./tj_dataset', [])

    avg_pairwise_precision = 0.0
    avg_pairwise_recall = 0.0
    avg_pairwise_f1 = 0.0
    # file_list = ['./tj_dataset/Keith Edwards.xml']
    

    for file in file_list:
        full_similarity_dict = dict()
        all_papers = generate_paper_instance_list(file)
        f_name = file+".txt"
        f_name = f_name.replace(".xml","")
        f_name =f_name.replace(" ","")
        File = open(f_name,"a")
        cnt = 0

        for paper in all_papers:

            #print (paper.paper_id)
            #print (paper.title)
            #print (paper.year)
            #print (paper.venue_id)
            #print (paper.affiliation_id)
            #print (paper.coauthors)
            #print (paper.author)
            t = ""
            for n in paper.coauthors:
            	t+=n
            	t+=","


            t = t[:-1]

            t.encode('utf8')

            if(paper.venue_id == None):
            	paper.venue_id = str(random.randint(1,2000000))

            if(paper.affiliation_id == None):
            	paper.affiliation_id = str(random.randint(1,20000))
            #print (str(cnt)+";"+str(paper.label)+";"+paper.author+";"+t+str(paper.title)+";"+str(paper.venue_id)+";"+str(paper.year)+"\n")
            File.write(str(cnt)+";"+str(paper.label)+";"+paper.author.encode("utf-8")+";"+t.encode("utf8")+";"+str(paper.title)+";"+str(paper.affiliation_id)+";"+str(paper.venue_id)+";"+str(paper.year)+"\n")

            cnt+=1
        File.close()