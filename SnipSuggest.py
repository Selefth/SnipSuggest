from random import *
import mysql.connector

DATABASE_HOST = "localhost"
DATABASE_USER = "root"
DATABASE_NAME = "SDSS"
DATABASE_PASSWD = "***"

mydb = mysql.connector.connect(
	host=DATABASE_HOST,
	user=DATABASE_USER,
	passwd=DATABASE_PASSWD,
	database=DATABASE_NAME
)

mycursor = mydb.cursor()

def find_feature_ids(features):
	fids = []
	for f in features:
		sql = "SELECT id FROM Features WHERE feature_description = '"+ f[1] +"' AND clause = '"+ f[2] + "'"
		mycursor.execute(sql)
		try:
			# feature is present, retrieve fid
			fids.append(str(mycursor.fetchone()[0]))
		except TypeError:
			continue
	return fids

def find_feature_description(fid):
	sql = "SELECT feature_description FROM Features WHERE id = '"+ fid +"'"
	mycursor.execute(sql)
	return mycursor.fetchone()[0]

def find_feature_clauses(features):
	clauses = []
	for f in features:
		clauses.append(f[1])
	return clauses

def clause(fid):
	sql = "SELECT clause FROM Features WHERE id = '"+ fid +"'"
	mycursor.execute(sql)
	return mycursor.fetchone()[0]

def snippets(suggestions):
	snippets = []
	for s in suggestions:
		sql = "SELECT feature_description FROM Features WHERE id = '" + str(s) +"'"
		mycursor.execute(sql)
		snippets.append(mycursor.fetchone()[0])
	return snippets

def ssaccuracy(m, fids):
	sql = "SELECT qf.feature FROM QueryFeatures qf, (SELECT query FROM QueryFeatures WHERE feature in ("+ ','.join(str(f) for f in fids) +") GROUP BY query having count(feature) = " + str(m)+") as sq WHERE qf.query = sq.query AND qf.feature NOT IN ("+ ','.join(str(f) for f in fids) +") GROUP BY qf.feature ORDER BY count(sq.query) DESC"
	rows = []
	mycursor.execute(sql)
	rows = mycursor.fetchall()
	return rows

def ssaccuracy_marg():
	sql = "SELECT * FROM MarginalProbs mp ORDER BY mp.probability DESC"
	rows = []
	mycursor.execute(sql)
	rows = mycursor.fetchall()
	return rows

def ssaccuracy_cond(fids, fdescr):
	sql = "SELECT id FROM Features f, (SELECT * FROM CondProbs) as cp, ((SELECT qf.feature FROM QueryFeatures qf, (SELECT query FROM QueryFeatures WHERE feature in ("+ ','.join(str(f) for f in fids) +") GROUP BY query) as sq WHERE qf.query = sq.query AND qf.feature NOT IN ("+ ','.join(str(f) for f in fids) +") GROUP BY qf.feature)) as nq WHERE f.feature_description = cp.feature1 AND f.id = nq.feature ORDER BY cp.probability DESC"
	rows= []
	mycursor.execute(sql)
	rows = mycursor.fetchall()
	return rows

def sscoverage(m, fids, previous):
	sql = "SELECT qf.feature FROM QueryFeatures qf, (SELECT query FROM QueryFeatures WHERE feature in ("+ ','.join(str(f) for f in fids) +") AND query NOT IN (SELECT query FROM QueryFeatures q WHERE q.query=query AND q.feature in ("+ ','.join(str(p) for p in previous) +")) GROUP BY query having count(feature) = " + str(m)+") as sq WHERE qf.query = sq.query AND qf.feature NOT IN ("+ ','.join(str(f) for f in fids) +") GROUP BY qf.feature ORDER BY count(sq.query) DESC"
	rows = []
	mycursor.execute(sql)
	rows = mycursor.fetchall()
	return rows

def get_suggestions(fids, clause_requested, k, technique):
	i = len(fids)
	suggestions = []
	while len(suggestions) < k and i >= 0:
		# marginal probs
		if len(fids) == 0:
			candidates = ssaccuracy_marg()
		# conditional probs
		elif len(fids) == 1:
			fdescr = find_feature_description(fids[0])
			candidates = ssaccuracy_cond(fids, fdescr)
		elif technique == "sscoverage" and len(suggestions) != 0:
			candidates = sscoverage(i, fids, suggestions)
		else:
			candidates = ssaccuracy(i, fids)
		for f in candidates:
			if str(f[0]) not in set(suggestions) and clause(str(f[0])) == clause_requested: suggestions.append(str(f[0]))
		i = i - 1
	return suggestions