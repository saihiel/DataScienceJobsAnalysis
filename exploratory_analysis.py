import pandas as pd
from ast import literal_eval
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
pd.set_option('display.max_columns', 50)

df = pd.read_csv('output_new.csv')
print(df.describe())
print(df.info())
print(df.head())

######################### Skills ###############################
def clean_skill_name(skill):
	new_skill = skill.replace(' (Programming Language)', '')
	new_skill = new_skill.replace('Amazon Web Services', 'AWS')
	if 'SQL' in new_skill:
		new_skill = 'SQL'
	new_skill = new_skill.replace('Microsoft Word', '')
	new_skill = new_skill.replace('Microsoft Excel', '')
	new_skill = new_skill.replace('Microsoft PowerPoint', '')
	new_skill = new_skill.replace('Microsoft Office', '')
	new_skill = new_skill.replace('Project Management', '')
	new_skill = new_skill.replace('Management', '')
	return new_skill

all_skills = df['Skills'].dropna().tolist()
all_skills = [clean_skill_name(skill) for sublist in all_skills for skill in literal_eval(sublist) if not clean_skill_name(skill)=='']

print('\nNumber of non-distinct skills: ', len(all_skills))
c = Counter(all_skills)
print(f'Number of distinct skills: {len(c.keys())}\n')
print('--'*25)
print("10 Most common Skills")
for entry in c.most_common(10):
	print(" Skill: {0:^20}\t Frequency: {1}".format(entry[0], entry[1]))
print('--'*25)

counts = np.array(list(c.most_common()))
print("\nNumber of Skills that appear exactly once: ",sum(counts[:,1]=='1'))
print("\nNumber of Skills that appear exactly twice:", sum(counts[:,1]=='2'))

def generate_skills_word_cloud(list_of_skills):
	# Make a word cloud for skills
	wordcloud = WordCloud(max_words=190, scale=10, mode='RGBA').generate(' '.join(list_of_skills))
	# Display the generated word cloud:
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()

# generate_skills_word_cloud(all_skills)

######################### Posting Age ########################################
def clean_posted_age(age_as_str):
	if not pd.isna(age_as_str):
		new_age_str = age_as_str.replace('Posted ', '').strip()
		multiplier = 7 if 'w' in new_age_str else 1
		multiplier = 30 if 'm' in new_age_str else multiplier
		return [int(s)*multiplier for s in new_age_str.split() if s.isdigit()][0] #Return the age in days
	else:
		return None


df['Posting Age In Days'] = df['Posting Age'].apply(lambda x: clean_posted_age(x))

def intersection(lst1, lst2):
	lst1_cleaner = [x.lower() for x in lst1]
	lst2_cleaner = [x.lower() for x in lst2]
	return list(set(lst1_cleaner) & set(lst2_cleaner))

def split_string_re(data):
	import re
	return re.findall(r"[\w']+", data)
######################### Position Title #####################################
def clean_position_title(position_as_str):
	if not pd.isna(position_as_str):
		position = split_string_re(position_as_str)
		analysts = ['Analyst', 'Scientist', 'Strategist', 'Advisor', 'Adviser', 'Designer', 'Integrator', 'Specialist' 
					'Analytics', 'Strategy', 'Architect', 'Researcher', 'Modeller', 'Modeler', 'Consultant', 'Research'
					'Associate', 'Model']
		senior = ['Senior', 'Lead', 'Director', 'Manager', 'Sr.', 'Deputy', 'II', 'III', 'Sr', 'Instructor']
		engineer = ['Engineer', 'Administrator', 'Full-Stack', 'Full Stack', 'Developer', 'Programmer']
		if len(intersection(position, senior))>0:
			if len(intersection(position, analysts))>0:
				new_position_as_str = 'Senior Analyst'
			elif len(intersection(position, engineer))>0:
				new_position_as_str = 'Senior Engineer'
			else:
				new_position_as_str = 'Technical Manager'
		elif len(intersection(position, engineer))>0:
			new_position_as_str = 'Engineer'
		elif len(intersection(position, analysts))>0:
			new_position_as_str = 'Analyst/Scientist'
		else:
			new_position_as_str = 'Other'
		if ('Intern' in position) or ('intern' in position):
			new_position_as_str = 'Intern'
		return new_position_as_str
	else:
		return None

df['Position Grouping'] = df['Position Title'].apply(lambda x: clean_position_title(x))

######################### Applicants Seniority ###############################
df['Applicants Seniority'] = df['Applicants Seniority'].apply(lambda x: literal_eval(str(x)) if not pd.isna(x) else x)

def seniority_list_to_dict(list_of_seniority_breakdown):
	all_levels = {'Entry Level %': 0, 'Senior Level %': 0, 'Manager Level %': 0, 'Director Level %': 0, 'VP Level %': 0}
	try:
		for level in list_of_seniority_breakdown:
			lst = level.split()
			applicant_level = lst[1]+' Level %' if not lst[1]=='CXO' else 'VP Level %'
			all_levels[applicant_level] += int(lst[0])
		total = sum(all_levels.values())
		for key,value in all_levels.items():
			all_levels[key] = format(100*(value/total), '.2f')
	finally:
		return pd.Series(all_levels, dtype='float64')
df2 = df['Applicants Seniority'].apply(lambda x: seniority_list_to_dict(x))
df2 = df2.replace(0, np.NaN)
df = pd.concat([df, df2], axis=1, sort=False)

######################### Applicants Education ###############################
df['Applicants Education'] = df['Applicants Education'].apply(lambda x: literal_eval(str(x)) if not pd.isna(x) else x)

def education_list_to_dict(list_of_education_breakdown):
	all_levels = {'Bachelor\'s %': 0, 'Master\'s %': 0, 'MBA %': 0, 'PhD %': 0, 'Other Degrees %': 0}
	try:
		for level in list_of_education_breakdown:
			level = level.replace('%% have','')
			lst = level.split()
			if 'Bachelor\'s' in lst:
				all_levels['Bachelor\'s %'] += int(lst[0])
			elif 'Master\'s' in lst:
				all_levels['Master\'s %'] += int(lst[0])
			elif 'Business' in lst:
				all_levels['MBA %'] += int(lst[0])
			elif 'Doctor' in lst:
				all_levels['PhD %'] += int(lst[0])
			elif 'other' in lst:
				all_levels['Other Degrees %'] += int(lst[0])
	finally:
		return pd.Series(all_levels, dtype='float64')

df2 = df['Applicants Education'].apply(lambda x: education_list_to_dict(x))
df2 = df2.replace(0, np.NaN)
df = pd.concat([df, df2], axis=1, sort=False)
print(df.describe(include='all'))

def create_box_plots():
	fig1, ax1 = plt.subplots()
	ax1.set_title('Applicants by Education Level')
	education_box_plot = df.boxplot(ax=ax1,
									column=['Bachelor\'s %', 'Master\'s %', 'MBA %', 'PhD %', 'Other Degrees %'])

	fig2, ax2 = plt.subplots()
	ax2.set_title('Applicants by Experience')
	experience_box_plot = df.boxplot(ax=ax2,
									 column=['Entry Level %', 'Senior Level %', 'Manager Level %', 'Director Level %',
											 'VP Level %'])

	fig3, ax3 = plt.subplots()
	ax3.set_title('Education Level by Position')
	education_by_position_box_plot = df.boxplot(ax=ax3, column=['Bachelor\'s %', 'Master\'s %'],
												by=['Position Grouping'])
	ax3.set_title('Education Level by Position')

	fig4, ax4 = plt.subplots()
	ax4.set_title('Education Level by Position')
	experience_by_position_box_plot = df.boxplot(ax=ax4, column=['Entry Level %', 'Senior Level %'],
												 by=['Position Grouping'])
	ax4.set_title('Education Level by Position')
	plt.show()

######################### Job Descriptions ###############################
import nltk
# nltk.download('wordnet')
# nltk.download('punkt') # one time execution
# nltk.download('stopwords')

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

sentences = []
for s in df['Job Description']:
	sentences.append(sent_tokenize(str(s)))

sentences = [y for x in sentences for y in x] # flatten list
# Extract word vectors
word_embeddings = {}
f = open('glove.6B/glove.6B.100d.txt', encoding='utf-8')
for line in f:
	values = line.split()
	word = values[0]
	coefs = np.asarray(values[1:], dtype='float32')
	word_embeddings[word] = coefs
f.close()

# remove punctuations, numbers and special characters
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

# make sentences lowercase
clean_sentences = [s.lower() for s in clean_sentences]


stop_words = stopwords.words('english')

# function to remove stopwords
def remove_stopwords(sen):
	sen_new = " ".join([i for i in sen if i not in stop_words])
	return sen_new

# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

sentence_vectors = []
for i in clean_sentences:
	if len(i) != 0:
		v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
	else:
		v = np.zeros((100,))
	sentence_vectors.append(v)
# similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])
from sklearn.metrics.pairwise import cosine_similarity
for i in range(len(sentences)):
	for j in range(len(sentences)):
		if i != j:
			sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

import networkx as nx

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
# Extract top 10 sentences as the summary
for i in range(10):
	print(ranked_sentences[i][1])