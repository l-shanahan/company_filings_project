#this code includes a number of tests of functions used in this project that will automatically be identified and run by pytest
#see readme for instructions on how to run

import sys
from utils import filepath_to_text, extract_text_between, text_breakdown

def test_filepath_to_text():

    """
    Testing the filepath_to_text function.
    """

    test_file_path = 'data/ibm.html'

    result = filepath_to_text(test_file_path)

    assert isinstance(result, str)

def test_extract_text_between():

    """
    Testing the extract_text_between function.
    """

    test_text = 'contents item 1. item 2. This is a test item 1. hello world ITEM 2. this is a test.'
    start_marker = 'Item\s+1\.'
    end_marker = 'Item\s+2\.'
    result = extract_text_between(test_text, start_marker, end_marker)

    assert result == ' hello world '

def test_text_breakdown():

    """
    Testing the text_breakdown function.
    """

    test_text = 'contents item 1. item 2. item 3. item 4. item 5. item 6. item 7. item 8. item 9. item 10. item 11. item 12. item 13. item 14. item 15. \
    item 1. hello item 2. item 3. item 4. item 5. item 6. item 7. item 8. item 9. item 10. item 11. item 12. item 13. item 14. world item 15.'

    result = text_breakdown(test_text)

    assert isinstance(result, list)
    assert result[0] == ' hello '
    assert result[-1] == ' world '
