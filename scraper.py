"""A web scraper for job postings on stack overflow filtering for python jobs."""
import requests
from bs4 import BeautifulSoup
import csv

if __name__ == '__main__':

    def parse_page(page):
        soup = BeautifulSoup(page.content, 'html.parser')
        jobs = soup.find_all(href='/jobs/developer-jobs-using-python')
        job_summaries = []
        for job in jobs:
            job_summaries.append(job.parent.parent.parent)

        with open('jobs.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            for job in job_summaries:
                title = job.find(class_='job-link').text
                company = job.find(class_='-name').text
                location = job.find(class_='-location').text
                date_posted = job.find(class_='-posted-date').text
                link = 'https://stackoverflow.com{}'.format(job.find(class_='job-link')['href'])
                writer.writerow([title, company, location, date_posted, link])

    for i in range(10):
        page = requests.get("https://stackoverflow.com/jobs?pg={}".format(i))
        parse_page(page)
