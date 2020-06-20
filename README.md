# Analysis of All Data Related Jobs on LinkedIn

While looking through countless jobs that are posted on LinkedIn on a daily basis, and looking through 'LinkedIn Premium Insights' on my fellow applicants, I decided to do an exploratory analysis on the postings and the applicant insights. This project consists of the following parts: 
  * Web Scrapping Jobs Postings and Applicant Insights from LinkedIn Jobs
  * Data Preprocessing and Exploratory Analysis on Scrapped Data
  * Conclusions drawn from analysis

## Web Scrapping LinkedIn Jobs
Unfortunately, LinkedIn does not make scrapping their website a trivial task. They update their website layout often and common web-scrappers found online wont cut it, or will likely get your account blocked. So I decided to use a scrapper I found online as a starting point and rebuild my own web-scrapper using selenium. I included a few tricks such as random mouse movements and delays between scrapes to make our web-scrapping bot seem more human-like. Once, I had built the scrapper built I decided to look for the most relevant job postings related to 'Data Science' and 'Data Analysis'. However, with these broad search terms postings related to 'Data Engineering', 'Data Modeling' and 'Financial Analysis' were also included in the scrape.
The raw scrapped data can be seen in the 'output_new.csv' file.

## Exploratory Analysis
The three main sections I explored are: 
  * Skills: The most common skills amongst all applicants
  * Education: The level of education of the applicants
  * Seniority (Experience): The level of experience of the applicants
The reason I selected these three features is becuase I feel they together give a good understanding of the types of applicants that we are completing against. By analysing the **most common skills amongst data practitioners** I found skills that I didn't have that I could now work on developing. The education level helped me consider the infamous question **'Higher Education vs Experience'**. Seniority tells us the amount of experience that most people have when applying for different positons. This allows us to align **ourselves, depending on our level of seniority**, to applying for the jobs that give us the best chance of success.

### Skills Section
I order to easily understand the most common skills amongst applicants I used a Word Cloud. This simple visually appealing representation exemplifies well the skills that most applicants proud themselves on. I will say that after aligning my skills on LinkedIn with the following skills (only the ones that I do really have), I have a *'Preferred Skills Badge'* on almost all the jobs I want to apply for. Now, I do not know how much of a difference this actually makes for employers, but I imagine it cannot hurt.

**The most common skill I found was Microsoft Office.** To be very honest, this came as a bit of a surprise to me. I expected something like 'Python', or 'Data Analysis' to be one of the most common skills. But, since Microsoft Office was a skill that was contained by almost every applicant, it skewed my results a little. Hence, I decided to create two seperate Word Clouds, one with Microsoft Office and other common 'general' skills such as 'Management' or 'Programming' and another with more Data Related skills. The code contained in the 'exploratory_analysis.py' file can make this more clear, as well as, the Word Clouds shown below. 
