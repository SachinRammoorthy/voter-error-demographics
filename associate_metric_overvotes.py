import csv

with open('tract_precinct_table.csv') as tract_precinct_table, open('input_data/rate_overvote.csv') as overvote_table, open('input_data/age.csv') as input_table, open('results/age_rov.csv', 'w') as result_table:

    tract_precinct_reader = csv.reader(tract_precinct_table, delimiter=',')
    overvote_reader = csv.reader(overvote_table, delimiter=',')
    input_table_reader = csv.reader(input_table, delimiter=',')
    result_writer = csv.writer(result_table, delimiter=',')
    
    prec_to_rov = {}
    census_dict = {}
    prec_to_count = {}

    for line in overvote_reader:
      prec_no = line[0]
      prec_to_rov[prec_no] = float(line[2]) / float(line[1]) if float(line[1]) != 0.0 else 0.0
    
    tract_to_census = {}
    top_row = []

    for row in input_table_reader:
      if row[1] == "Total":
        top_row = row
        top_row[0] = "precinct_id"
        top_row[1] = "rate_overvote"
        continue

      tract_id = row[0] if '.' not in row[0] else row[0][:-3]
      if tract_id not in tract_to_census:
        # for education
        # tract_to_census[tract_id] = [0,0,0,0,0,0,0]

        # for age
        tract_to_census[tract_id] = [0,0,0,0]

        # for poverty, sex
        # tract_to_census[tract_id] = [0,0]

        # for income
        # tract_to_census[tract_id] = [0]

      for i in range(len(row[2:])):
        tract_to_census[tract_id][i] += int((row[2:])[i])
    
    tract_to_area = {}
    seen = set()
    for row in tract_precinct_reader:
      if row[1] == 'Tract_ID':
        continue
      tract_id = row[1] if '.' not in row[1] else row[1][:-3]
      if '.' in row[1] and row[1] not in seen:
        if tract_id in tract_to_area:
          tract_to_area[tract_id] += int(row[8])
        else:
          tract_to_area[tract_id] = int(row[8])
        seen.add(row[1])
      elif '.' not in row[1]:
        tract_to_area[tract_id] = int(row[8])

    prec_to_metric = {}
    tract_precinct_table.seek(0)
    for row in tract_precinct_reader:
      if row[1] == "Tract_ID":
        continue
      tract_id = row[1] if '.' not in row[1] else row[1][:-3]
      percentage_tract = float(row[9]) / float(tract_to_area[tract_id])

      prec_id = row[2]
      if prec_id not in prec_to_metric:
        # for education
        # prec_to_metric[prec_id] = [0,0,0,0,0,0,0]

        # for age
        prec_to_metric[prec_id] = [0,0,0,0]

        # for poverty, sex
        # prec_to_metric[prec_id] = [0,0]

        # for income
        # prec_to_metric[prec_id] = [0]
      
      for i in range(len(prec_to_metric[prec_id])):
        prec_to_metric[prec_id][i] += percentage_tract * int(tract_to_census[tract_id][i])
    
    result_writer.writerow(top_row)

    for key, value in prec_to_metric.items():

      # only for rate-based metrics. Comment for income
      total = 0
      for i in value:
        total += i
      for i in range(len(value)):
        value[i] = value[i] / total

      value.insert(0, key)
      if key in prec_to_rov:
        value.insert(1, prec_to_rov[key])
        result_writer.writerow(value)
      else:
        print(f"Not available for precinct {key}")
