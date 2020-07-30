# LinkedIn Job Parser
This program scrapes linkedin.com jobs search to find the common programming languages
pertaining to popular careers in computer science. This program takes about 10-20 minutes to 
go through all of the data. Once the data is exported into a CSV file, there is a console program
'plotData.py' which can visually present the data.
* **Run 'getData.py' first to get data**
* **Run 'plotData.py' after getting data**
# Packages
* pandas
* bs4 (BeautifulSoup)
* selenium (Webdriver, Exceptions, Keys, and Chrome)
* time
* os
* sklearn (prepossessing)
# Example 
Partial CSV file (There are more programming languages and career positions): <br />

Programming Languages |DATA SCIENCE | SOFTWARE DEV | NETWORKS | DATABASES | WEB DESIGN 
----------------------|-------------|--------------|----------|-----------|-----------
Java | 14 | 70 | 3 | 8 | 20
C++ | 4 | 50 | 30 | 19 | 0 
Python| 33 | 102 | 43 | 24 | 9
SQL | 18 | 13 | 40 | 130 | 1 
HTML/CSS | 3 | 38 | 0 | 0 | 98 
* This example does not represent the true data found.
* Data that did not have a job title relating to the position was ignored. With
this being said, we had to scaled the data when working the data with sklearn preprocessing<br />
<br />
Partial CSV files with count pertaining to each job:<br />

 Count/Missed Data |DATA SCIENCE | SOFTWARE DEV | NETWORKS | DATABASES | WEB DESIGN 
-------------------|-------------|--------------|----------|-----------|-----------
Count | 124 | 173 | 58 | 21 | 104
Missed Data | 69 | 300 | 38 | 83 | 13
* This example does not represent the true data found.
* The count represents the jobs that were accounted for.
* The missed data is the data that raised an error or was skipped because the title did not match
job keywords.
## Contact
 Phone: (971) 708-4444<br />
 Email: ericsanderson333@gmail.com<br />
 Linkedin: https://www.linkedin.com/in/ericanderson333 <br />
 Please contact me and send me any questions/advice! Thanks!








