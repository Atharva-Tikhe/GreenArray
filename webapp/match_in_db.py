import os
import mysql.connector as mysql
from dotenv import load_dotenv
import pandas as pd
import re
from sqlalchemy import create_engine
# function placeholder for irl file input
# new_file = 'processed_57385_v1-full.tsv'
# reference = 'processed_56878_v1-full_wc.tsv'

load_dotenv('./webapp/project.env')
conn = mysql.connect(host='localhost', user = 'root', passwd = os.getenv('PASS'), db = 'nbs')
curs = conn.cursor(buffered=True)

class MatchWithDb:
    def __init__(self, reference, new_file):
        self.new_file = new_file
        self.reference = reference
        self.new_df = pd.read_csv(self.new_file, sep='\t', header=2)
        self.ref_df = pd.read_csv(reference, sep='\t')
        self.preprocess_new_df()
        self.process_dataframes()

    def preprocess_new_df(self):
        self.new_df.insert(allow_duplicates=True, loc = 13, value = 0, column = 'allele_frequency_%_corrected')
        self.new_df.insert(allow_duplicates=True, loc = 14, value = 0, column = 'zygosity')
        self.new_df.insert(allow_duplicates=True, loc = 15, value = 1, column = 'entry_count')

        corr_freq = self.new_df.loc[:, ['allele_frequency_%']]

        drop_index = []
        for index,value in corr_freq['allele_frequency_%'].items():
            val = re.search('[ATGCatgc=]', value)
            if val is not None:
                drop_index.append(index)

        self.new_df.drop(drop_index, inplace = True)
        corr_freq.drop(drop_index, inplace = True)

        # populate corrected freq column
        corr_freq = corr_freq.astype('float')

        corr_freq = corr_freq.apply(lambda x: 100 - x)

        self.new_df['allele_frequency_%_corrected'] = corr_freq

        df_snp = self.new_df[self.new_df['type'] == 'SNV']
        homozygous = df_snp['allele_frequency_%_corrected'].map(lambda x: 'homozygous' if x < 10 else 'heterozygous' )
        df_snp['zygosity'] = homozygous
        self.new_df.update(df_snp)

        df_indel = self.new_df[self.new_df['type'] == 'INDEL']
        zygosity = df_indel['allele_frequency_%_corrected'].map(lambda x: 'homozygous' if x < 20 else 'heterozygous')
        df_indel['zygosity'] = zygosity
        self.new_df.update(df_indel)

        self.new_df.to_csv(f'webapp/samples/processed_{self.new_file.split("/")[-1]}', sep='\t', index = False)


    def process_dataframes(self):

        self.common = pd.merge(self.ref_df, self.new_df, how='inner', left_on=['# locus', 'zygosity', 'genotype'], right_on=['# locus', 'zygosity', 'genotype'], suffixes=('', '_y'))

        common_locus = self.common['# locus']

        if len(common_locus) != 0:
            ref_df_common_index = []
            new_df_common_index = []
            for locus in common_locus:
                ref_df_common_index.append(self.ref_df[self.ref_df['# locus'] == locus].index)
                new_df_common_index.append(self.new_df[self.new_df['# locus'] == locus].index)

            for index in ref_df_common_index:
                self.ref_df.iloc[index, 15] += 1

            for index in new_df_common_index:
                self.new_df.drop(index, inplace=True)

        result = pd.concat([self.ref_df,self.new_df], ignore_index=True)

        result.to_csv(self.reference, sep='\t', index=False)

        engine = create_engine(f"mysql+mysqlconnector://root:{os.getenv('PASS')}@localhost/nbs")
        result.to_sql('variants', engine, 'nbs', if_exists='replace')


