#!/usr/bin/env python
import pandas as pd
import operator as o

import time

print "----Start COFFS----"
# execution metrics
start_time = time.time()

# config | column position in csv input file for age in months, weight, height, sex
source_data_file = 'data/sample.csv'
output_data_file = 'data/sample_comp.csv'
col_age = 'age'
col_weight	= 'weight'
col_height	= 'height'
col_sex	= 'sex'

# config | csv delimiter
csv_delimiter = ';'

# config | decimal mark | comma for EU+ and dot for US+
decimal_mark = ','

#config | active references
compute = ['who','iotf']

# config | references
ref = { 'iotf' : {'cutoffs' : pd.Panel({ 'F' : pd.read_csv('references/IOTF_f.txt', sep='\t', header=0), 'M': pd.read_csv('references/IOTF_m.txt', sep='\t', header=0) }),
				'labels' : [{'label' : 'thinness grade 2', 'cutoff' : '17', 'comparison' : '<'},
							{'label' : 'thinness grade 1', 'cutoff' : '18.5', 'comparison' : '<'},
							{'label' : 'normal', 'cutoff' : '25', 'comparison' : '<'},
							{'label' : 'overweight', 'cutoff' : '30', 'comparison' : '<'},
							{'label' : 'obesity', 'cutoff' : '35', 'comparison' : '<'},
							{'label' : 'morbid obesity', 'cutoff' : '35', 'comparison' : '>='}],
				'month' : 'Age (months)'
				},
		'who' : {'cutoffs' : pd.Panel({ 'F' : pd.read_csv('references/WHO_f.txt', sep='\t', header=0), 'M' : pd.read_csv('references/WHO_m.txt', sep='\t', header=0) }),
				'labels' : [{'label' : 'severely thin', 'cutoff' : 'SD3neg', 'comparison' : '<'},
							{'label' : 'thin', 'cutoff' : 'SD2neg', 'comparison' : '<'},
							{'label' : 'normal', 'cutoff' : 'SD1', 'comparison' : '<'},
							{'label' : 'overweight', 'cutoff' : 'SD2', 'comparison' : '<'},
							{'label' : 'obese', 'cutoff' : 'SD3', 'comparison' : '<'},
							{'label' : 'severely obese', 'cutoff' : 'SD3', 'comparison' : '>='}],
				'month' : 'Month'
				}
		}

# config | operator map
operator_map = { '<': o.lt, '<=': o.le, '==': o.eq, '>': o.gt , '>=': o.ge }

# -------------- end of CONFIG -------------------

# load data input
data = pd.read_csv(source_data_file, sep = csv_delimiter, header=0, decimal = decimal_mark)
print "Loaded %s rows from file %s" % (len(data.index), source_data_file)

# process | calculate BMI and append to dataframe
print "Compute BMI"
data['comp_bmi'] = data[col_weight]/(data[col_height]/100)**2

# check label for row
def put_label(source, row, bmi):
	for val in ref[source]['labels']:
		if operator_map[val['comparison']](bmi, row[val['cutoff']].iloc[0]):
			label = val['label']
			break
	return label

# label calculation
def comp_labels(x):
	age_round = int(round(x[col_age]))
	
	results = {}

	for source in compute:		
		row = ref[source]['cutoffs'][x[col_sex]].loc[ref[source]['cutoffs'][x[col_sex]][ref[source]['month']] == age_round]
		if row.shape[0] ==1:
			results['comp_'+source+'_label'] = put_label(source, row, x['comp_bmi'])
		else:
			results['comp_'+source+'_label'] = "age out of bound"

	return pd.Series(results)
# ------------------------------------------------

print "Compute label for references %s" % (compute, )
data = pd.concat([data, data.apply(lambda x: comp_labels(x), axis=1)], axis=1)

# save to csv
print "Save results to file %s" % output_data_file
data.to_csv(output_data_file, sep = csv_delimiter, index = False, decimal = decimal_mark)

# execution metrics
execution_time = time.time() - start_time
print "Total execution time %s" % execution_time
print "----End COFFS----"
