from webapp.match_in_db import MatchWithDb



with open('./assets/sample-matrix.tsv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        filename, gender = line.strip().split('\t')
        if gender == "Male" or gender == 'M':
            obj = MatchWithDb('webapp/processed_56878_v1-full_wc.tsv', f'assets/inputs/{filename}', 'M')
        elif gender == "Female" or gender == 'F':
            obj = MatchWithDb('webapp/processed_56878_v1-full_wc.tsv', f'assets/inputs/{filename}', 'F')
        else:
            raise ValueError(f"Gender '{gender}' is not recognized")
