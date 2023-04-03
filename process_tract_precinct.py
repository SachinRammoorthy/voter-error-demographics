import csv

# file to process tract-precinct relation data

with open('overlap_table.csv') as csv_file, open('processed_overlap_table.csv', 'w') as updated_table:
    csv_reader = csv.reader(csv_file, delimiter=',')

    tract_normalization_val = {}
    prec_map = {}

    all_lines = []
    for row in csv_reader:
      all_lines.append(row)


    # first pass
    # combine 101.01 and 101.02 -> 101
    combined_tract_areas = {}
    seen_tracts = set()
    for i in range(len(all_lines)):
      row = all_lines[i]
      
      if i != 0:
        tract_name = str(row[1])
        tract_area = float(row[4])
        percentage_tract = float(row[5]) # percent of the tract that the overlap area comprises

        if tract_name not in seen_tracts:
          new_tract_name = tract_name
          if "." in tract_name:
            new_tract_name = tract_name[:tract_name.find(".")]

          if new_tract_name in combined_tract_areas:
            combined_tract_areas[new_tract_name] += tract_area
          else:
            combined_tract_areas[new_tract_name] = tract_area
        
          seen_tracts.add(tract_name)
    
    # get the new percentage_tracts for each overlap area
    for i in range(len(all_lines)):
      row = all_lines[i]
      
      if i != 0:
        tract_name = str(row[1])
        if "." in tract_name:
          tract_name = tract_name[:tract_name.find(".")]
          all_lines[i][1] = tract_name
        
        overlap_area = float(row[3])
        
        # new percentage_tract
        all_lines[i][5] = overlap_area / combined_tract_areas[tract_name]
        # new tract area
        all_lines[i][4] = combined_tract_areas[tract_name]

    # now, 101.01 doesn't exist. condensed to 101
    
    # correcting for water area.
    # i.e, if percentage_tract don't add up to 1
    
    for i in range(len(all_lines)):
      row = all_lines[i]
      if i == 0:
        continue
      # correct %tract
      tract_name = str(row[1])
      percentage_tract = float(row[5]) # percent of the tract that the overlap area comprises
      if tract_name not in tract_normalization_val:
        tract_normalization_val[tract_name] = percentage_tract
      else:
        tract_normalization_val[tract_name] += percentage_tract

    # tract A -> 50% in ocean
    # tract_normalization_val[A] = 0.5

    # tract B -> 100% accounted for by precincts
    # tract_normalization_val[B] = 1.0001
    
    for key, value in tract_normalization_val.items():
      tract_normalization_val[key] = 1 / value
    
    # tract_normalization_val[A] = 2
    # tract_normalization_val[B] = 1
    
    cvs_writer = csv.writer(updated_table, delimiter=',')
    for i in range(len(all_lines)):
      row = all_lines[i]
      if i != 0:
        row[5] = float(row[5]) * tract_normalization_val[str(row[1])]
      cvs_writer.writerow(row)
    
    print("Job Finished.")