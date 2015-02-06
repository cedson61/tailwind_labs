import pandas as pd
import numpy as np

OUTPUT_COLUMNS = (
    # the summary stats to be calculated for each column in the input csv file
    'column_name',
    'data_type',
    'pct_missing',
    'pct_unique',
    'min',
    'max',
    'mean',
    'most_frequent'
)

DISPLAYABLE_COLUMNS = (
    'CSV Column',
    'Data Type',
    'Percent Missing',
    'Percent Unique',
    'Minimum',
    'Maximum',
    'Mean',
    'Most Frequent'                       
)


class CSVSummary(object):
    """
    Read a csv file directly into a pandas DataFrame. Calculate summary stats for each column,
    and prepare them in a python dict.
    
    """

    def __init__(self, input_file_name):
        self.df = pd.read_csv(input_file_name)          # read the csv into a pandas dataframe
        self.column_names = self.df.columns.tolist()    # list of column names in the csv input file
        self.csv_row_count = len(self.df.index)         # number of rows in the csv input file

        self.output = {}
        self.output['header'] = OUTPUT_COLUMNS
        self.output['rows'] = []

        for column_name in self.column_names:
            
            row = {} # a python dict with the OUTPUT_COLUMNS as keys

            row['column_name'] = column_name

            row['data_type'] = self.df[column_name].dtype

            col_non_blanks = float(self.df[column_name].count())
            row['pct_missing'] = "%.1f" % (100 * (1 - (col_non_blanks / self.csv_row_count)))
             
            row['pct_unique'] = "%.1f" % (100.0 * self.df[column_name].nunique() / self.csv_row_count)
            
            row['min'] = self.df[column_name][pd.notnull(self.df[column_name])].min()

            row['max'] = self.df[column_name][pd.notnull(self.df[column_name])].max()

            if (self.df[column_name].dtype != object):
                row['mean'] = "%.1f" % (self.df[column_name].mean())
            else: # can't calculate a numeric mean for non-numeric columns
                row['mean'] = '--' 

            row['most_frequent'] = self.df[column_name].value_counts().idxmax()

            self.output['rows'].append(row)


if __name__ == "__main__":

    input_file_name = 'olympic_medals_2.csv'

    data = CSVSummary(input_file_name)

    output_list = []
#    for row in modata.output['rows']:
#        output_list.append([])
#        for col in OUTPUT_COLUMNS:
#            output_list[row].append()
            
    print data.output['header']
          
    row_list = []
    for row in data.output['rows']:
        rlist = []                      # convert each row to an ordered list of values
        for col in OUTPUT_COLUMNS:
            rlist.append(row[col])
        row_list.append(rlist)     # append the row to the list

    for i in row_list:
        print i

#    print ', '.join(data.output['header']), '\n'
#
#    for row in data.output['rows']:
#        for col in OUTPUT_COLUMNS:
#            print '%s, ' % row[col], 
#        print '\n'

