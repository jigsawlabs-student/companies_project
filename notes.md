# General notes.

Overall, when looking at the some of the aggregate functions in the models, I would prefer if you:
1. Lean on SQL as opposed to Python (although it's great practice that you were able to perform in Python)
But, SQL is generally faster, and I think will may make the code simpler
2. Simplify the functions
  a) One way to simplify the function is instead of say performing aggregate methods for a 
  list of companies, only perform for a single company.  And then loop through that method 
  to calculate the aggregate for each company you need.
  b) When the functions grow longer than five lines long, break them into multiple steps.
  When it feels like the function is going to be more than 10 lines long, take a step back and see 
  if you can simplify your goals for the function.  (Eg. do for one company instead of many)

3. get_companies_info.py
  a) The data_ingestion_processing folder feels like a junk drawer.  Some of the files there feel quite useful, and other
  code looks like it is not used at all.  Identify good locations for files that are used and remove the files that are not used.
  b) for example, the `get_companies_info.py` file contains a Client, so move it to the adapters folder, and perform create a builder for it.
  currently the builder functionality for intrinio is located in the CompanyBuilder file.

4. Frontend
It looks like the index.py file is still a work in progress, and not quite ready for review.  
However, I do like many of the "Functions written in Jan".  The only issue is avg_element_wise_list function.
This function should be in the backend, as it performs a calculation, and I believe may already be performed by one of your other aggregate functions.

I would divide this frontend into multiple files.  So a lot of the functions should be moved to a separate file still in the frontend folder, and then imported when needed.

5. Very nice  start with the tests.

6. Just remember to delete functions and files if they are not used.  If you prefer, you can move them to files outside of your project repository.
For example, prototyping_map_reduce.py, potentitally old_sp_500_folder (if not used), some of the files in data_ingestion_processing.
