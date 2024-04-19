# Current state of the project

Here is a doc that can be used as an overview of the project. One should thus be able to see what exactly needs working on at this current time. The main benefit lies in the simplicity of this documentation process.

### Scraping and downloading data

Currently, there are a few areas to work on regarding scraping and downloading data.

- Savings and Sentiment are targeted only by a specific URL, which should be improved (using some element type for xpath etc.) ⛔
- GrossWage and MedianWage are targeted only by a specific URL, which should be improved (using some element type for xpath etc. ⛔

### Processing the data

Below are the specific subsections of the code that need to be addressed with their current state.

- Grouping and ordering the input files ✅
- Wages ✅
- Unemployment ✅
- Household debt ✅
- Household disposable income ✅
- Employment potential ✅
- Commodities (Gas.py and Electricity.py) ✅

  - to Solve: Input files have the .xls suffix that makes them unavailable for using polars, there is also no package included that solves this issue and the files currently need to be saved as .xlsx manually
  - to Solve: Available data include only the current year resulting in the need to merge with some older dataset(s)
  - to Solve: Complete the output file for both Gas and Electricity
- Standardizing the time dimensions for the whole project ⛔
- Optimizing the code ⛔
