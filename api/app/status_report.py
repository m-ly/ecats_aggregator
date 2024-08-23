import pandas as pd
import xlrd
import os

### USAGE ###
# The Filename will need to include what position the the report is tracking
# When running the script, the argument passed to the script is the absolute path of the folder where the reports are stored

# given a directory as an input
    #For each xls file in the the directory, create a frame, and push the frame to an array
    # transform each element in the array to desired formatting - rename column
    # merge the frames into a single frame
    # write the frame to excel

DIRECTORY = './uploads'
# The file name must include one of these exact strings in the name 
POSITIONS = ['fire', 'phones', 'ch1','ch2', 'training']

def create_status_report():
  
  def set_working_file(filename):
    wb = xlrd.open_workbook(filename, logfile=open(os.devnull, 'w'))
    data = pd.read_excel(wb)
    wb.release_resources()
    del wb
    return data

  ###todo
  # def format_position_name(str_val):
  #   # if the filename includes a string in positions. Lowercase the string, and return a constant format matching  a standard value 
  #   return 

  def set_position_name(filename, positions):
    for ele in positions:
      if ele.lower() in filename:
        return ele

  def column_index(search_value, frame):
    for column in frame.columns:
      if (frame[column] == search_value).any():
        return frame.columns.get_loc(column)

  def row_index(search_value, frame):
    for column in frame.columns:
      if (frame[column] == search_value).any():
        index = frame.loc[frame[column] == search_value].index[0]
        return index
        
  def create_iter_range(start_row, end_row):
    result = []
    for index in range(start_row, end_row, 2):
      result.append(index)
    return result

  def current_working_data(frame):
    user_column_index = column_index('Agent', frame)
    total_time_column_index = column_index('Logged On', frame)
    start_row = row_index('Agent', frame) + 2
    end_row = row_index('Overall:', frame) - 1

    filters = [user_column_index, total_time_column_index]
    rows_range = create_iter_range(start_row, end_row)

    return frame.iloc[rows_range, filters]


  def agent_time_df(filename, frame):
    agents = {}
    position = set_position_name(filename, POSITIONS).title()
    for _index,row in frame.iterrows():
      agents[row.iloc[0].title()] = format_time(row.iloc[1])
    return pd.DataFrame({'Agents': list(agents.keys()), position: list(agents.values())})

  def format_time(number_string):
    numbers = number_string.split(':')
    numbers = [int(i) for i in numbers]
    if len(numbers) == 4:
      return round(((( numbers[0] * 24 + numbers[1] ) * 60 ) + numbers[2] ) / 60, 2)
    
    return round((numbers[0] * 60 + numbers[1]) / 60, 2)


  def all_reports(directory):
    xls_files = [];
    for root_, dir_, files in os.walk(directory):
      for file in files:
        if file.endswith(".xls"):
          xls_files.append(directory + '/' + file)
    return xls_files

  def create_frame(file):
    try: 
      input_data = set_working_file(file)
      filtered_data = current_working_data(input_data)
      return  agent_time_df(file,filtered_data)
    except Exception as e:
      print(f"Error processing file {file}: {e}")
      return None

  def report_writer(directory):
    reports = all_reports(directory)
    frames = []

    for file in reports:
      frames.append(create_frame(file))

    # Concatenate all frame objects, grouping on the Agent key
    merged_frame = pd.concat(frames, axis=0)
    result = merged_frame.groupby('Agents').sum()
    result.reset_index(inplace=True)

    # Alphabetize columns
    result = result.reindex(sorted(result.columns), axis=1)

    # Add a row for the sum of all numbers in the current rows
    sum_of_data = result.copy()
    result['Total Hours'] = sum_of_data.sum(numeric_only=True, axis=1)

    # Insert new column tracking percentage between hours 
    for i in range(result.shape[1] - 1, 1, -1):
          col_name = f"{result.columns[i - 1]} %"
          result.insert(i, col_name, round(result.iloc[:, i - 1] / result.iloc[:, -1], 2))

    with pd.ExcelWriter(path = DIRECTORY + "/monthly_status_report.xlsx") as writer:
      result.to_excel(writer, index=False)
 

  report_writer(DIRECTORY)