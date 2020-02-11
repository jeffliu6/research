import urllib.request as urllib
from bs4 import BeautifulSoup

# title	text	year	month	day	link	issue.NO	cum.issue
# import csv
# import codecs
#
#
# def load():
#     with codecs.open('qiushi-data.csv', 'rb', encoding="utf-8-sig") as csvfile:
#         reader = csv.DictReader(csvfile)
#
#         count = 0
#         for row in reader:
#             if row['text'] is None:
#                 count += 1


'''
Full data set
Extend to as much as possible. All of 2017 and 2018.
Fill in missing articles (as much as possible) (URLs are there already)
Website: http://www.qstheory.cn/qs/mulu.htm
Clean text
Make sure that the text is as clean as possible from html junk.
Remove intro and concluding extraneous text (if present)
'''


def get_year_links():
    '''
        get links to every year's issues
    '''
    input_url = "http://www.qstheory.cn/qs/mulu.htm"
    page = urllib.urlopen(input_url)
    soup = BeautifulSoup(page,'html.parser')
    titles = soup.find_all(class_="booktitle")
    years = []
    for title in titles:
        child = next(title.children)
        years.append(child['href'])

    years_tuple_dict = []
    for year in years:
        if year[len(year)-3:] == 'htm': #2014 and later
            years_tuple_dict.append((year, 'new'))
        # elif year[len(year)-1:] == '4': #2004
        #     years_tuple_dict.append((year, 'oldest'))
        else:
            years_tuple_dict.append((year, 'old'))
    return years_tuple_dict


def get_issue_links(input):
    '''
        given url for a year, get all the issues for that year
    '''
    issues = []
    input_url = input[0]

    if input[1] == 'new':
        page = urllib.urlopen(input_url)
        soup = BeautifulSoup(page,'html.parser')
        highlight = soup.find(class_='highlight')
        paragraphs = highlight.find_all('a')
        for paragraph in paragraphs:
            link = paragraph['href']
            if 'mulu' not in link:
                issues.append(link)
    # elif input[1] == 'oldest':
    #     page = urllib.urlopen(input_url)
    #     soup = BeautifulSoup(page,'html.parser')
    #     paragraphs = soup.find_all(class_='qihao_qs')
    #     for paragraph in paragraphs:
    #         sublink = paragraph.find('a')['href']
    #         issues.append(input_url + '/' + sublink[2:])
    elif input[1] == 'old':
        page = urllib.urlopen(input_url)
        soup = BeautifulSoup(page,'html.parser')
        paragraphs = soup.find_all(class_='qihao_qs')
        for paragraph in paragraphs:
            sublink = paragraph.find('a')['href']
            issues.append(input_url + '/' + sublink[2:])
    return issues



def scrape():
    '''
        Scrape data from 2004 - 2020 and convert to CSV form
        2013 and earlier has 1 form
        2014 and later has a 2nd form
    '''
    years_dict = get_year_links()
    issues = []
    for year in years_dict:
        one_year_issues = get_issue_links(year)
        issues.extend(one_year_issues)

    for issue in issues:
        print(issue)
    # for year in years:
        # issues.append(get_issue_links(year))

    #
    # issues.append(get_issue_links(years[0]))


if __name__ == "__main__":
    # data = load()
    data = scrape()
