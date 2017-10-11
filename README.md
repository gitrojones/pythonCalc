# Python Calc
**REQUIRES PYTHON >3**
Tested on version 3.5.2

Small calculator app put together for fun. Uses string manipulation to build a list of operations based on the rules of PEDMAS in order to allow for natural chained statements.
## Issues
1) Order of Operations fails to recognize second-degree operations. IE. 7-2+20/2 results in an array of [7-[2+20]/2] where it should read [7-[[2+20]/2]]. Likely a small fix I may get around to in the future.
2) Debug information is pretty messy. Will likely fix in the future.
## Tests
Some test coverage in place. 
