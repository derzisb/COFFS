# COFFS

A simple python script for computing weight labels for children, using cut-offs references produced by health organizations.
At the current moment two cut-offs references are used:

 - *WHO 2007* - available from [WHO REF]
 - *IOTF 2012* - available from [IOTF REF]

## Installation

COFFS requires [Pandas] library. You can install pandas using *pip* or the other methods specified in the [docs].

	pip install pandas

You can get the latest version of COFFS with the command:

    git clone https://github.com/dragulescubogdan/COFFS.git

## How to

To run the script just type the following command from the project root:
    
    python coffs.py

The script uses the sample.csv file provided in the data directory and saves the results in the sample_comp.csv. The computed labels (BMI, WHO label, IOTF label) are appended to the original columns from the sample.csv file. 

To use your data file, change the *source_data_file* setting to point to it. Also, change the *output_data_file* setting to the desired value. The source data file needs to be in csv format. The default delimiter is ';', but you can change it in the *csv_delimiter* setting. 

    source_data_file = 'path/to/your/file.csv'
    output_data_file = 'path/to/your/output_file.csv'
    csv_delimiter = 'csv delimiter'

The minimum columns needed to compute the weight labels are: *age* in months (default: 'age'), *weight* in kilograms (default: 'weight'), *height* in cm (default: 'height') and *sex* capital letters M or F (default: 'sex'). If you want to change the default column names you can do so by modifying the appropriate settings in the coffs.py file. You can leave extra columns in the file, the script will leave them intact and append the computed values. 
	
    col_age = 'new age column'
    col_weight	= 'your weight column'
    col_height	= 'new height column'
    col_sex	= 'new sex column'

If you use a dot for the decimal mark in float numbers, change the *decimal_mark* setting from ',' to '.'. 

    decimal_mark = '.'

## License

COFFS was created by Bogdan Dragulescu to help Adela Chirita in her studies.
It's MIT [licensed]. Maybe someone else finds the script useful.

[WHO REF]: http://www.who.int/growthref/who2007_bmi_for_age/en/
[IOTF REF]: http://www.worldobesity.org/aboutobesity/child-obesity/newchildcutoffs/
[Pandas]: http://pandas.pydata.org/
[docs]: http://pandas.pydata.org/pandas-docs/version/0.16.2/install.html
[licensed]: https://github.com/dragulescubogdan/COFFS/blob/master/LICENSE