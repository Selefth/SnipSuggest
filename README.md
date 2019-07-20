# SnipSuggest
Final Database project. Master in Big data and Artificial Intelligence. Department of Informatics and Telecommunications of the University of Athens. Submitted 20/07/2019.

/SS creation/

1. Run query_eliminator.py to clean the log data file result.csv
2. Run query_repo.py to create the relations snip suggest uses
3. Load the data to MySQL with data_loader
4. Run main and ask for recommendations
   Examples:
	1)empty query, press enter (MarginalProbs activated)
	2)select ra/ from/ 5/ssaccuracy or sscoverage (CondProbs activated)
	3)from photoprimary/ select/ 30/ sscoverage
	4)from photoprimary/ select/ 30/ ssaccuracy
	5)from specobj/ group by/ 3/ ssaccuracy
	etc

/Experiments/

1. Run test_data_producer.py that use the test_queries.csv
2. Run experiments.py
