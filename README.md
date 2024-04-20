# Financial filings processing repository

This is a repository of code that processes HTML files of SEC US public company filings to extract key information. For a specific path containing relevant HTML files and a specific dictionary containing a description of information which the user would like to extract from said files, the code will produce and write JSON files for each HTML file containing a summary of the requested information. The code requires a working OpenAI API key, as relatively inexpensive API calls to gpt-3.5-turbo are made.

## How to run

1) To run this code the config file should first be updated:
- For the 'data_directory' field, the value should be the path name (str) of the folder that contains the HTML files the user wishes to process. If left as 'data', the example HTML files stored in this repository will be processed.
- The 'openai_key' field should include a working OpenAI API key (str) with permission to use the gpt-3.5-turbo model.
- The 'info_dict' field should include a dictionary containing the information which the user would like to extract from the HTML files. The keys in this dictionary should be the title of each piece of information (str), while the value should be a brief description of the information which the user would like to extract from the document.

2) Ensure all the required packages are installed (check the requirements.txt file)

3) Navigate to the root directory in terminal and run python3 main_code.py

4) The output will be JSON files for each input HTML file containing the description of the information which the user wanted to extract as keys and the results/output for that information as values. These JSON files are saved to the output folder.

## Design choices

I decided to use available large language models (gpt-3.5-turbo) to process the text from each file and generate the summaries. The reasons for choosing this method over any alternatives (eg. using regex to separate the text or searching for certain html delimiters to separate the original documents) are as follows:

1) Flexiblity of information required - with my method, the user can chose any information which they would like from the file. The information can be complex or difficult to comprehend, they only need to input this information into the config file and they will recieve some kind of output.

2) Flexibility in filetype analysed - this method could in future be applied to company filings with different or unusual formats since LLMs will still be able to comprehend these (compared to something like regex which could only be applicable to set file formats. Regex might also fail easily if certain expressions don't appear in other files). However, regex is still used in my code to separate the documents into more manageable chunks. In future, a different method could be used to separate into chunks (e.g. by number of characters), to enable the code to be more universably flexible.

## Default output

If the `info_dict` in the config is not changed, it will by default output the following:

Business Summary (str): A brief business summary describing the company and its key products
Office Summary (str): A description of the location and offices of the company
Risk Assessment (str): A description of the main risks facing the company
Core Products (str): A list of the core products produced by the company
Industry (str): A description of the industry that the company primarily operates within
Financial Summary (str): A summary of the financial performance of the company over the past year

From reading through the example filings, these categories seemed like a good summary of the useful content in each. These topics are likely to be of interest to anyone inspecting the company filings to get an understanding of a specific company.

After running the code locally, I stored the resulting output JSON files in the 'example outputs' folder. This is for anyone who does not have the resources to run the code themselves to visualise the output.

## Running tests

To run the automated tests for this code, you will need to have the version of `pytest` installed given in the requirements.txt file. Once pytest is installed, navigate to the root directory of the project in terminal and run: 

`pytest`
