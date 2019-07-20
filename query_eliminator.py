from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.word2vec import Word2Vec
import pandas as pd
import numpy as np
import re

def W2Vec(statement):
	queries = [re.split(r"select|from|where|group by", s) for s in statement]
	model = Word2Vec(queries, window=5, min_count=4, workers=8)
	# model.save("word2vec.model")
	w2v = dict(zip(model.wv.index2word, model.wv.syn0))
	w2v_statement = np.array([np.mean([w2v[q] for q in query if q in w2v] or\
	 [np.zeros(model.vector_size)], axis=0) for query in queries])
	return w2v_statement

def DeleteRow(df,indexes):
	df = df.drop(df.index[indexes])
	df.reset_index(drop=True, inplace=True)
	return df

def ZeroPadding(a):
	if int(a)<10:
		a="0" + str(a)
		return a
	else:
		return str(a)

def cleaner1(path,n="ALL"):
	df = pd.read_csv(path, engine="python", error_bad_lines=False)
	df = df.replace("\n","", regex=True).dropna()
	df.reset_index(drop=True, inplace=True)
	if n=="ALL": return df
	return df.head(n)

def cleaner2(statement,w):
	statement = statement.replace("(?<![A-Za-z0-9.])([0-9][.0-9]+)", "#", regex=True).str.lower()
	statement = statement.replace("(?<![A-Za-z0-9.])([0-9]+)", "#", regex=True)
	statement = statement.str.wrap(w)
	return statement

def cleaner3(df, statement):
	badWords=["0x","@","htmid","create","having","order by","between","not in","left","outer","inner","join","href","http"]
	indexes=[]
	for i, r in statement.iteritems():
		for b in badWords:
			if b in r: indexes.append(i)
	df = DeleteRow(df,indexes)
	return df

def cleaner4(df,theta):
	w2v_statement = W2Vec(df["statement"])
	while True:
		indexes=[]
		for i,j in zip(range(0,df.shape[0]-1,2),range(1,df.shape[0],2)):
			if (df["theTime"][i][:8] == df["theTime"][j][:8]) & (df["clientIP"][i] == df["clientIP"][j]):
				u = w2v_statement[i].reshape(1,-1)
				v = w2v_statement[j].reshape(1,-1)
				if cosine_similarity(u,v) >= theta:
					indexes.append(i)
			else: continue
		old = df.shape[0]
		df = DeleteRow(df,indexes)
		new = df.shape[0]
		w2v_statement = np.delete(w2v_statement, [indexes], axis=0)
		if old == new: break
	return(df)

def cleaner5(theTime):
	delimiters = "[/|:| ]"
	for i,r in theTime.iteritems():
		time = r.strip()
		tokens = re.split(delimiters,time)
		if "" in tokens:
			tokens = tokens.remove("")
		tokens[0] = ZeroPadding(tokens[0])
		tokens[1] = ZeroPadding(tokens[1])
		tokens[2] = ZeroPadding(tokens[2])
		tokens[3] = ZeroPadding(tokens[3])
		tokens[4] = ZeroPadding(tokens[4])
		tokens[5] = ZeroPadding(tokens[5])
		if tokens[6] == "PM":
			tokens[3] = str(int(tokens[3])+12)
		removeAM_PM = tokens[0:6]
		timeValue = "".join(removeAM_PM)
		theTime.set_value(i, timeValue)
	return theTime

if __name__ == "__main__":
	# Queries relation
	Queries = cleaner1(".../result.csv")
	Queries["statement"] = cleaner2(Queries["statement"],800)
	Queries = cleaner3(Queries, Queries["statement"])
	Queries = cleaner4(Queries,0.6)
	Queries["theTime"] = cleaner5(Queries["theTime"])
	Queries.insert(0, "qid", range(Queries.shape[0]))
	# Queries.to_excel(".../Queries.xlsx", index=False)