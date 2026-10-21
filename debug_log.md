# Debug log (Part A)

Name: Aiden Ford   Date: October 21, 2026

Fill one block per ticket, in the order you fixed them. Use the method from the lesson: Reproduce, Read,
Isolate, Hypothesise, Test, Fix, Verify. Short answers are fine, but the EVIDENCE line must be something
you actually saw (a pdb command and its output, or a print line).

## BUG-1
- Symptom (what I saw): BUG-1: BUG-1: median of an even-sized list
3
- Family (syntax / runtime / logic): Logic
- Hypothesis (before I looked): It's returning the mean not the median
- Evidence (pdb command + output, or print output): 
(Pdb) ordered
[1, 2, 3, 4]
- Root cause (one sentence): It does not account for cases where there is an even amount of numbers
- Fix (one sentence): Add a new return statement with correct logic in the case of even length input
- Verified by:

## BUG-2
- Sympton: BUG-2: BUG-2: top 3 slowest tests
[340, 210]
- Family: Logic
- Hypothesis: However it's set up is returning the opposite amount of answers (asking for 0 gives almost whole list)
- Evidence:  (Pdb) p n - 1
2
- Root cause: Should be returning up to n variables, not n - 1
- Fix: Remove the -1, add catches for edge cases (longer n than list and n = 0)
- Verified by:

## BUG-3
- Symptom: Crashes with a KeyError
- Family: Runtime
- Hypothesis: The code is not checking if the key it is using actually exists or not
- Evidence: (Pdb) p grouped
{}
- Root: grouped starts out with zero keys
- Fix: Check for if that key exists or not, same with status
- Verified by:

## BUG-4
- Symptom: BUG-4: BUG-4: two separate reports each keep a flaky list
(['t2', 't9'], ['t2', 't9'])
- Family: Logic
- Hypothesis: Each function call is sharing the same list
- Evidence: 
(Pdb) p flaky
['t2']
(Pdb) c
> c:\users\aford\desktop\qea-testing-folder\week2_wed\run_stats.py(88)note_flaky()
-> return flaky
(Pdb) p flaky
['t2', 't9']
- Root: The same flaky list is being used across each function call
- Fix: Default flaky to None, change it to empty list if it passed in as None
- Verified by:

## BUG-5
- Symptom: Crashes with an UnboundLocalError
- Family: Runtime
- Hypothesis: Trying to access a variable that does not exist in the function
- Evidence: (Pdb) pp locals()
{}
- Root: There are no local variables, the variable it is trying to access does not exist locally
- Fix: Add global declaration for run_counter at start of function
- Verified by:

## BUG-6
- Symptom: 
BUG-6: BUG-6: the dashboard summary, 'latest' test duration
{'run_id': 'RUN-0001', 'total': 4, 'by_suite': {'login': {'pass': 2, 'fail': 1}, 'search': {'pass': 1}}, 'median_ms': 135.0, 'slowest_ms': [340, 210, 150], 'latest_ms': 80}
- Family: Logic
- Hypothesis: It's sorting the whole list of durations and then returning the shortest one
- Evidence:  (Pdb) p durations
[340, 210, 150, 120, 95, 80]
- Root: It's returning the last value like it should but the slowest() function sorts it first
- Fix: Change slowest() so that it sorts a new copy of the list instead of the original one
- Verified by:

## BUG-7
- Symptom: Crashes with ValueError
- Family: Runtime
- Hypothesis: Doesn't deal with the possibility of empty list
- Evidence: List was empty in passing
- Root: Multiple calls to the list were not valid since the list was empty (for example can't do list[-1] on empty list)
- Fix: Add if else checks to make sure duration contains something
- Verified by:

## Reflection (3 sentences)
The hardest to find was BUG-3, I think dealing with the traceback at first was the hardest. Breakpoint helped the most since I could stop the code at any time and see what was going on. Next time I would read the code properly beforehand to know what its function is.
