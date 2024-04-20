#all the functions required to process the html files into raw text, segregate them into manageable chunks for input into gpt, 
#create outputs for all the required info types using gpt and save them as JSON files in the output folder

from bs4 import BeautifulSoup
import re
from openai import OpenAI
import os
import json


def filepath_to_text(file_path):
  """
  Converts html file specified by given file path into raw text, removing 
  html formatting using beautifulsoup.
  Inputs: 
  file_path (str) = path of html file to be processed
  Outputs:
  text (str) = processed raw text
  """
  try:
      with open(file_path, 'r', encoding='utf-8') as file:
          html_content = file.read()
  except UnicodeDecodeError:
      with open(file_path, 'r', encoding='latin-1') as file:
          html_content = file.read()

  soup = BeautifulSoup(html_content, 'html.parser')
  text = soup.get_text(separator=' ', strip=True)
  return text


def extract_text_between(text, start_marker, end_marker):

  """
  Selects all text between second occurrence of start marker text
  and second occurence of end marker text using regex. Designed to be
  used with 'item n.' text which appears once in contents and once as heading.
  Inputs: 
  text (str) = raw text to be processed
  start_marker (str) = expression to start cutting text from
  end_marker (str) = expression to end cutting text from 
  Outputs:
  text (str) = processed raw text between second occurrences of markers
  """

  start_matches = [match for match in re.finditer(start_marker, text, re.IGNORECASE)]
  end_matches = [match for match in re.finditer(end_marker, text, re.IGNORECASE)]

  if len(start_matches) < 2 or len(end_matches) < 2:
      print("Not enough occurrences of start or end marker found.")
      return None

  start_index = start_matches[1].end()
  end_index = end_matches[1].start()

  return text[start_index:end_index]


def text_breakdown(text):

  """
  Breaks down passage of raw text into list of segmented text. Text segmented between 
  item headings.
  Inputs: 
  text (str) = raw text to be processed
  Outputs:
  text_list_trimmed (list of strings) = list where each element is section of input text separated between item headings
  """

  item_list = ['Item\s+1\.','Item\s+2\.','Item\s+3\.','Item\s+4\.','Item\s+5\.','Item\s+6\.','Item\s+7\.','Item\s+8\.','Item\s+9\.','Item\s+10\.','Item\s+11\.','Item\s+14\.','Item\s+15\.']
  i = 0
  j = 1
  text_list = []
  while j < len(item_list):
    start_marker = item_list[i]
    end_marker = item_list[j]
    section_text = extract_text_between(text, start_marker, end_marker)
    text_list.append(section_text)
    i += 1
    j += 1
  max_length = 20000
  text_list_trimmed = [s[:max_length] for s in text_list]
  return text_list_trimmed


def summary_creator(text, previous_summary, info_desc, openai_key):

  """
  Given a summary of a certain type of information about a company that must be found that already exists,
  this function uses that summary, along with a passage of text, to write a new summary about that type of information
  based off any additional information from the passage of text. The function uses both the current summary and the
  passage of text to compose a prompt to gpt-3.5-turbo, which it calls via the API.
  Inputs: 
  text (str) = the passage of text
  previous_summary (str) = the summary so far
  info_desc (str) = the type of information/question which the model will try to write the new summary about
  openai_key (str) = a valid API key for the OpenAI API
  Outputs:
  combined_summary (str) = the new summary generated using all the information available
  """

  client = OpenAI(api_key=openai_key)

  prompt = f"I am going to provide you with a 'summary' of the key information about the following task: {info_desc}. \
  I am then going to provide you with a 'passage' of text which may or may not include additional information on that task. \
  Please re-write the summary to include any additional information from the passage of text. It is possible that the initial summary will \
  contain no text, in which case use the information in the passage of text to write a summary. If there is no information in \
  the passage of text relevant to the task, do not update the summary. Summary: {previous_summary}. Passage of text: {text}"

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant, skillful at analysing passages of texts and summarising key findings."},
      {"role": "user", "content": prompt}
    ]
  )

  combined_summary = completion.choices[0].message.content

  return combined_summary


def all_items_summary(text_list_trimmed, info_desc, openai_key):

  """
  Loop runs through a list of text strings. For each string, it writes a new summary using the text from that string
  and an already existing summary about a type of information given as input. The existing summary starts as empty space,
  so the summary for the first string in the list will only use that string to determine the new summary. Final summary after
  running through the entire list will be given as output. The 'updated summary' will therefore iteratively improve given
  the new information from each string in the list.
  Inputs: 
  text_list_trimmed (list of strings) = list of strings of text to be used to create final summary
  info_desc (str) = a description of the type of information which we want the summary to be about
  openai_key (str) = a valid API key for the OpenAI API
  Outputs:
  summary (str) = the final summary about the target information using all the text in the input list
  """

  summary = ''

  for i in text_list_trimmed:
    updated_summary = summary_creator(i, summary, info_desc, openai_key)
    summary = updated_summary

  return summary


def info_types_summary(info_list, text_list_trimmed, openai_key):

  """
  For a list of information types and a list of strings, this function uses the information from the list of strings to write
  summaries about each of the information types in the list.
  Inputs: 
  info_list (list of strings) = list containing descriptions of a number of information types
  text_list_trimmed (list of strings) = list of strings of text to be used to create summary for each information type
  openai_key (str) = a valid API key for the OpenAI API
  Outputs:
  summary_list (list of strings) = list of the responses/summaries for each of the input information types
  """

  summary_list = []
  for i in info_list:
    info_type_summary = all_items_summary(text_list_trimmed, i, openai_key)
    summary_list.append(info_type_summary)

  return summary_list


def info_to_result(filepath_list, info_dict, openai_key):

  """
  This function loops through a list of filepaths containing html files. For each file, it writes a summary/response 
  for required information also given as input and returns a list of these summaries.
  Inputs: 
  filepath_list (list of strings) = list containing filepaths of html files to be processed
  info_dict (dict) = a dictionary containing the type of information which should be produced as keys and a description of
  how to find that type as values
  openai_key (str) = a valid API key for the OpenAI API
  Outputs:
  The function saves a JSON file for each input filepath in the 'output' directory
  """

  info_title_list = list(info_dict.keys())
  info_desc_list = list(info_dict.values())
  for filepath in filepath_list:
    company_text = filepath_to_text(filepath)
    text_list = text_breakdown(company_text)
    results_list = info_types_summary(info_desc_list, text_list, openai_key)
    output_dict = dict(zip(info_title_list, results_list))

    filename = os.path.basename(filepath)
    json_filename = filename.replace('.html', '.json')
    output_directory = 'output'
    output_filepath = os.path.join(output_directory, json_filename)
    with open(output_filepath, 'w') as f:
      json.dump(output_dict, f)
      print(f"{filename} JSON saved")
