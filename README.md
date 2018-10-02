# Carbon Black Response: Intel Tester
This script is designed to take a json collection of Carbon Black Response queries and run them day by day to review total matches per day. This can be used to test out new IOC's, baseline user/process behaviors and much more. The script works by taking a list of queries defined in your `config.json` file and using your defined start date to run a day by day check on each query. The results are saved to a csv file for you to review. 

This script is related to the blog post: https://blog.stillztech.com/2018/10/carbon-black-response-intel-tester.html 

## Usage
Update the config.json with your Carbon Black URL and API token. then update the `queries` section of the json file with the queries you'd like to test. Lasty, specify the `year`, `month` and `day` you wish the start the test. 
> python main.py

