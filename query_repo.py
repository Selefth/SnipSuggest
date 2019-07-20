import query_eliminator as el
from itertools import combinations
import pandas as pd
import numpy as np
import re

def ClausesTokenizer(i, s):
	features = []

	try:
		select_clause = re.search(r"(?<=select)(.*)(?=from)",s).group(0)
		select_features = SelectFeatures(select_clause)
		features += [[i, f, "select"] for f in select_features]
	# invalid query
	except AttributeError: features += []

	try:
		from_clause = re.search(r"((?<=from)(.*)(?=(where|group by)))|((?<=from)(.*))",s).group(0)
		from_features = FromFeatures(from_clause)
		features += [[i, f, "from"] for f in from_features]
	# invalid query
	except AttributeError: features += []

	a = re.search(r"(?<=group by)(.*)",s)
	b = re.search(r"((?<=where)(.*)(?=(group by)))|((?<=where)(.*))",s)

	if a is not None:
		group_by_clause = re.search(r"(?<= group by)(.*)",s).group(0)
		groupBy_features = GroupByFeatures(group_by_clause)
		features += [[i, f, "group by"] for f in groupBy_features]

	if b is not None:
		where_clause = re.search(r"((?<=where)(.*)(?=(group by)))|((?<=where)(.*))",s).group(0)
		where_features = WhereFeatures(where_clause)
		features += [[i, f, "where"] for f in where_features]

	return features

def balancedString1(word):
	count = 0
	flag = True
	records = []
	n = len(word)

	# Maintain a count for opening
	# brackets Traversing string
	for i in range(n):

		# check if opening bracket
		if (word[i] == "("):
			flag = False
			records.append(i)
			count += 1

		# check if closing bracket and count != 0
		elif (word[i] == ")" and count != 0 and flag == False):
			del records[-1]
			count -= 1

		# if word[i] not a closing brackets
		elif (word[i] == ")"):
			flag = True
			records.append(i)
			count += 1

		else: continue

	# balanced brackets if opening brackets
	# are more then closing brackets
	if (count != 0):
		tokens = list(word)
		for i in sorted(records, reverse=True):
		    del tokens[i]
		word = "".join(tokens)
	return word

def balancedString2(sentence):
	balance = 0
	parts = []
	part = ""

	for s in sentence:
		part += s
		if s == "(":
			balance += 1
		elif s == ")":
			balance -= 1
			part = part.replace(" ", "")
		elif s == "," and balance == 0:
			parts.append(part[:-1].strip())
			part = ""

	# Capture last part
	if len(part):
		parts.append(part.strip())
	return parts

def SelectFeatures(sentence):
	clean = []

	# both are clauses that go with select
	if "top #" in sentence: 
		sentence = sentence.replace("top #", "")
	if "distinct" in sentence:
		sentence = sentence.replace("distinct", "")

	parts = balancedString2(sentence)

	for p in parts:
		p = re.sub(r"[a-z]*\.|\.","",p)
		p = re.sub(r" as [a-z]*","",p)
		clean.append(p)
	return clean

def FromFeatures(sentence):
	clean = []
	parts = balancedString2(sentence)

	# Delete all after " "
	for p in parts:
		p = p.split(" ")[0]
		p = p.replace(".", "")
		clean.append(p)
	return clean

def WhereFeatures(sentence):
	parts = [f for f in re.split(r" and | or ", sentence)]

	clean = []
	for p in parts:
		f = re.sub(r"[a-z]\.|\.","",p)
		f = balancedString1(f)
		clean.append(f.replace(" ", ""))
	return clean

def GroupByFeatures(sentence):
	return [f.strip() for f in sentence.split(",")]

def MarginalProbs(W, Features, QueryFeatures):
	probs = []
	u_fids = Features["fid"].values.tolist()
	qf_ids = QueryFeatures.tolist()
	for u in u_fids:
		qids = []
		for qf in qf_ids:
			if u == qf[1]: 
				qids.append(qf[0])
		probs.append([u, len(qids)/W])
	return probs

def CondProbs(W, MarginalProbs, Features, QueryFeatures):
	fset = []
	Featlist = Features[["feature_description", "clause"]].values.tolist()
	# find any possible feat combination based on clause
	temp1 = [f[0] for f in Featlist if f[1] == "select"]
	temp2 = [f[0] for f in Featlist if f[1] == "from"]
	temp3 = [f[0] for f in Featlist if f[1] == "where"]
	temp4 = [f[0] for f in Featlist if f[1] == "group by"]
	fset += [subset for subset in combinations(temp1,2)]
	fset += [subset for subset in combinations(temp2,2)]
	fset += [subset for subset in combinations(temp3,2)]
	fset += [subset for subset in combinations(temp4,2)]

	probs = []
	for f in fset:
		# [0] since fid1 & fid2 are unique
		fid1 = Features.index[Features["feature_description"] == f[0]].values.tolist()[0]
		fid2 = Features.index[Features["feature_description"] == f[1]].values.tolist()[0]

		# with [0] we take the list
		qid1_i = np.where(QueryFeatures[:,1] == fid1)[0]
		qid2_i = np.where(QueryFeatures[:,1] == fid2)[0]

		qid1 = QueryFeatures[qid1_i, 0]
		qid2 = QueryFeatures[qid2_i, 0]
		qids = np.intersect1d(qid1, qid2)

		mpf1_i = np.where(MarginalProbs[:,0] == fid1)[0][0]
		mpf2_i = np.where(MarginalProbs[:,0] == fid2)[0][0]

		mpf1 = MarginalProbs[mpf1_i, 1]
		mpf2 = MarginalProbs[mpf2_i, 1]

		probs.append([f[0], f[1], (qids.shape[0]/W)/mpf2])
		probs.append([f[1], f[0], (qids.shape[0]/W)/mpf1])

	return probs

def DeleteDuplicates(df):
	df = df.drop_duplicates()
	df.reset_index(drop=True, inplace=True)
	return df

def ExcelFile(path, dflist, cnames):
	df = pd.DataFrame(dflist, columns=cnames)
	df.to_excel(path, index=False)

if __name__ == "__main__":
	# Queries relation
	Queries = el.cleaner1(".../result.csv")
	Queries["statement"] = el.cleaner2(Queries["statement"],800)
	Queries = el.cleaner3(Queries, Queries["statement"])
	Queries = el.cleaner4(Queries,0.6)
	Queries["theTime"] = el.cleaner5(Queries["theTime"])
	Queries.insert(0, "qid", range(Queries.shape[0]))
	# Queries.to_excel(".../Queries.xlsx", index=False)

	# Feature relation
	features=[]
	for i,s in Queries["statement"].iteritems():
		features += ClausesTokenizer(i,s)
	temp1 = pd.DataFrame(features, columns=["qid", "feature_description", "clause"])
	Features = DeleteDuplicates(temp1[["feature_description", "clause"]])
	temp2 = Features.values.tolist()
	Features.insert(0, "fid", range(Features.shape[0]))
	# Features.to_excel(".../Features.xlsx", index=False)

	# QueryFeatures relarion
	ids = []
	for i,un_fset in enumerate(temp2):
		for fset in features:
			if un_fset == fset[1:]: ids.append([fset[0],i])
	QueryFeatures = np.asarray(ids)
	# ExcelFile(".../QueryFeatures.xlsx", ids, cnames=["qid","fid"])

	# MarginalProbs relation
	wload_cardinality = Queries.shape[0]
	probs = MarginalProbs(wload_cardinality, Features, QueryFeatures)
	MarginalProbs = np.asarray(probs)
	# ExcelFile(".../MarginalProbs.xlsx", probs, cnames=["fid", "probability"])

	# CondProbs relation
	cprobs = CondProbs(wload_cardinality, MarginalProbs, Features, QueryFeatures)
	CondProbs = np.asarray(cprobs)
	# ExcelFile(".../CondProbs.xlsx", cprobs, cnames=["feature1", "feature2", "probability"])