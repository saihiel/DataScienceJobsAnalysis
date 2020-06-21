# Analysis of Data Related Jobs on LinkedIn

While looking through countless jobs that are posted on LinkedIn on a daily basis, and looking through 'LinkedIn Premium Insights' on my fellow applicants, I decided to do an exploratory analysis on the postings and the applicant insights. This project consists of the following parts: 
  * Web Scrapping Jobs Postings and Applicant Insights from LinkedIn Jobs
  * Data Preprocessing and Exploratory Analysis on Scrapped Data
  * Conclusions drawn from analysis

## Web Scrapping LinkedIn Jobs
Unfortunately, LinkedIn does not make scrapping their website a trivial task. They update their website layout often and common web-scrappers found online wont cut it, or will likely get your account blocked. So I decided to use a scrapper I found online as a starting point ([reference](https://github.com/nicolomantini/Linkedin-Job-Scraper)) and rebuilt it into my own web-scrapper with selenium. I included a few tricks such as random mouse movements and delays between scrapes to make our web-scrapping bot seem more human-like. Once, I had built the scrapper built I decided to look for the most relevant job postings related to 'Data Science' and 'Data Analysis'. However, with these broad search terms postings related to 'Data Engineering', 'Data Modeling' and 'Financial Analysis' were also included in the scrape.
The raw scrapped data can be seen in the 'output_new.csv' file.

## Exploratory Analysis
The three main sections I explored are: 
  * Skills: The most common skills amongst all applicants
  * Education: The level of education of the applicants
  * Seniority (Experience): The level of experience of the applicants  

The reason I selected these three features is becuase I feel they together give a good understanding of the types of applicants that we are completing against. By analysing the **most common skills amongst data practitioners** I found skills that I didn't have that I could now work on developing. The education level helped me consider the infamous question **'Higher Education vs Experience'**. Seniority tells us the amount of experience that most people have when applying for different positons. This allows us to **align ourselves, depending on our level of seniority**, to applying for the jobs that give us the best chance of success.

## Skills Section
I order to easily understand the most common skills amongst applicants I used a Word Cloud. This simple visually appealing representation exemplifies well the skills that most applicants proud themselves on. I will say that after aligning my skills on LinkedIn with the following skills (only the ones that I do really have), I have a *'Preferred Skills Badge'* on almost all the jobs I want to apply for. Now, I do not know how much of a difference this actually makes for employers, but I imagine it cannot hurt.

**The most common skill I found was Microsoft Office.** To be very honest, this came as a bit of a surprise to me. I expected something like 'Python', or 'Data Analysis' to be one of the most common skills. But, since Microsoft Office was a skill that was contained by almost every applicant, it skewed my results a little. Hence, I decided to create two seperate Word Clouds, one with Microsoft Office and other common 'general' skills such as 'Management' or 'Programming' and another with more Data Related skills. The code contained in the 'exploratory_analysis.py' file can make this more clear, as well as, the Word Clouds shown below. 

### Technical Skills
![DS Skills](https://github.com/saihiel/DataScienceJobsAnalysis/blob/master/Word%20Clouds/Specialized%20Skills.png)

### All Skills
![General Skills](https://github.com/saihiel/DataScienceJobsAnalysis/blob/master/Word%20Clouds/General%20Skills.png)

### Most Common Skills
Additionally, a bar graph with the 10 most common technical skills from the *approximately 350+ scrapped postings*:
![Technical Skills Bar Graph](https://github.com/saihiel/DataScienceJobsAnalysis/blob/master/Technical_Skills.png)

## Education Section
In this section I looked to answer the question about the proportion of applicants with a **Bachelors Degree vs Masters Degree**, broken up by job type. I found that the clearest way to represent this was with the box plot shown below. Clearly, and as expected the people applying for Analyst/Scientist more commonly had a Masters Degree than a Bachelors Degree. The median amount applicants with a Masters was 50% while the medium amount with a Bachelors was ~35%. 

However, for Engineering positions this was closer with Masters applicants making up about 47% and Bachelors applicants around 40%. As expected, for Senior positions the proportion of applicants with Bachelors Degrees is significantly lower.

![Education Breakdown](https://github.com/saihiel/DataScienceJobsAnalysis/blob/master/Box%20Plots/Positions%20by%20Education.png)

## Experience Section
In this section I wanted to understand the breakdown of applicants by their level of experience for various positions. The first thing we notice here is that, as expected, applicants for senior positions tend to have more experience. However, we also notice that there is a higher proportion of Entry level applicants is higher than that of Senior applicants for Engineer positions, but roughly the same for Analyst/Scientist positions. 
*One possible explanation could be that since we found more applicants for Analyst/Scientist positions to have a Masters Degree, as a result of being in school longer, they have less experience under their belts?*

![Experience Breakdown](https://github.com/saihiel/DataScienceJobsAnalysis/blob/master/Box%20Plots/Positions%20by%20Experience.png)

**Do you want to see some different analysis on this dataset? Send me an email** [**here**](mailto:saihiel.bakshi@mail.utoronto.ca)
