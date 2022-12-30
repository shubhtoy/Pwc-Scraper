# Description: This script will scrape all the jobs from PWC website and save it in a json file.
# Author: @shubhtoy
# Version: 1.0
# Python Version: 3.11.0

# importing the required libraries
import requests
import json
import re
from threading import Thread


# Defining the constants
OUTPUT_FILE = "output.json"

# Defining the global variables
all_jobs = []
base_url = "https://www.pwc.in/careers/experienced-jobs/results.html"
jd_url = "https://www.pwc.in/careers/experienced-jobs/description.html"


# Defining the functions
cookies = {
    "_fbp": "fb.1.1672414757476.139711321",
    "ln_or": "eyIzNzU1NTcyIjoiZCJ9",
    "AMCVS_93091C8B532955160A490D4D%40AdobeOrg": "1",
    "_ga": "GA1.2.100333572.1672414758",
    "_gid": "GA1.2.1566787448.1672414758",
    "s_cc": "true",
    "ak_bmsc": "2AE31C90BB1AC9020F10976E2454ECFA~000000000000000000000000000000~YAAQLrYRYNg8gUmFAQAA5UYgZBLD/9hFde6zhgCYfsGKZbnHuYPStjIFGsLCZwRcbNF3lUW6f2eaBaOxneq9vwchTDL8o9Pgxp3V7FfYAhBflei4veeGoeMZ0hSTs4r0pn4lCKU5KdvrVIPdy2KBdfcQjYQtNIO4PIclFJ3fZMTQlxB1VP2e/LyISQn3kBMkdtN7FUXy0DvUGTcpM8j/HD2YNbXkHFKAAW5SCApnLBNaPv7rRfGzhxJgDxJLdnju7mP80LQye3m53daADL3ggULw0U5WTm2mgEbCQb0DONfW+ER0Rprbc807wftPIsDsOyRcLVFzMta9xdrKjEU0KHjjzOvYOBJ7iavjIJfh5uWEIsW0S1f7UZYH38utYTxqt3rE+BOeLALU/w==",
    "AMCV_93091C8B532955160A490D4D%40AdobeOrg": "-408604571%7CMCIDTS%7C19357%7CMCMID%7C48992693728843879794405777416188076450%7CMCAAMLH-1673028145%7C12%7CMCAAMB-1673028145%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1672430546s%7CNONE%7CMCSYNCSOP%7C411-19364%7CvVersion%7C4.6.0",
    "s_nr": "1672427280243-Repeat",
    "gpv": "in%7Ccareers%7Cexperienced-jobs%7Cresults.html",
    "s_ppvl": "in%257Ccareers%257Cexperienced-jobs.html%2C60%2C52%2C1820%2C1039%2C760%2C1536%2C864%2C1.25%2CP",
    "s_sq": "%5B%5BB%5D%5D",
    "bm_sv": "C4B1810536DCEE63DC642E8BF267A59C~YAAQINYsF9JENGGFAQAA8hlvZBL56rvU7WAKJvKlWYXzVeE+m+n/wJ67t14JHvjXtJnL1dNdJS1ZdMq2i4nlQ+KNmx+qLc7DZSec48p+f+2MOej8vz6wUup0HSryC15+tRO/BODDsuqN9VXMM10OQdY11bLcOcgPdAT8WslC1p65V2F2htBkl2xkZGM6Dx2clr0IBC6uQYO8Y0ep6brLFBLDnrPkB8vrrIYOpQscair6et81Q1KrOoPuwLdkasEY0A==~1",
    "s_ppv": "in%257Ccareers%257Cexperienced-jobs%257Cresults.html%2C37%2C22%2C1290%2C1039%2C760%2C1536%2C864%2C1.25%2CP",
}


headers = {
    "authority": "www.pwc.in",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    # 'cookie': '_fbp=fb.1.1672414757476.139711321; ln_or=eyIzNzU1NTcyIjoiZCJ9; AMCVS_93091C8B532955160A490D4D%40AdobeOrg=1; _ga=GA1.2.100333572.1672414758; _gid=GA1.2.1566787448.1672414758; s_cc=true; ak_bmsc=2AE31C90BB1AC9020F10976E2454ECFA~000000000000000000000000000000~YAAQLrYRYNg8gUmFAQAA5UYgZBLD/9hFde6zhgCYfsGKZbnHuYPStjIFGsLCZwRcbNF3lUW6f2eaBaOxneq9vwchTDL8o9Pgxp3V7FfYAhBflei4veeGoeMZ0hSTs4r0pn4lCKU5KdvrVIPdy2KBdfcQjYQtNIO4PIclFJ3fZMTQlxB1VP2e/LyISQn3kBMkdtN7FUXy0DvUGTcpM8j/HD2YNbXkHFKAAW5SCApnLBNaPv7rRfGzhxJgDxJLdnju7mP80LQye3m53daADL3ggULw0U5WTm2mgEbCQb0DONfW+ER0Rprbc807wftPIsDsOyRcLVFzMta9xdrKjEU0KHjjzOvYOBJ7iavjIJfh5uWEIsW0S1f7UZYH38utYTxqt3rE+BOeLALU/w==; AMCV_93091C8B532955160A490D4D%40AdobeOrg=-408604571%7CMCIDTS%7C19357%7CMCMID%7C48992693728843879794405777416188076450%7CMCAAMLH-1673028145%7C12%7CMCAAMB-1673028145%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1672430546s%7CNONE%7CMCSYNCSOP%7C411-19364%7CvVersion%7C4.6.0; bm_sv=C4B1810536DCEE63DC642E8BF267A59C~YAAQLrYRYCQ+gkmFAQAAZNIzZBKtA29JrnF5tx5pPam3P0lu78SuMh5p+ZIt4hVj8p8kYGl4PNGLjZdpdD46x4lPE8pPqho0ifPKdSWGURUfrR6AnYOz5dmmzu3GSC+gow6tV6+wZ6Ora2e3V3/UFcR6imhfFXw3t9VMYnnPKp3G+YlcowoXwz+owVqcvfPImFqqPw2z+6rfCLlgjlUs3Rx6CYt6QvHYh8M9KmP8NAqx02FvoBC/7zntHufGsCCb~1; gpv=in%7Ccareers%7Cexperienced-jobs%7Cresults.html; s_ppvl=in%257Ccareers%257Cexperienced-jobs%257Cdescription.html%2C36%2C16%2C1692%2C1039%2C760%2C1536%2C864%2C1.25%2CP; s_ppv=in%257Ccareers%257Cexperienced-jobs%257Cresults.html%2C57%2C27%2C66232%2C1039%2C760%2C1536%2C864%2C1.25%2CP; s_nr=1672423582045-Repeat; s_sq=pwcglobalweb%252Cpwcin%3D%2526c.%2526a.%2526activitymap.%2526page%253Din%25257Ccareers%25257Cexperienced-jobs%25257Cresults.html%2526link%253DAssociate%252520-%252520SFDC%2526region%253Dwdresults%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Din%25257Ccareers%25257Cexperienced-jobs%25257Cresults.html%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.pwc.in%25252Fin%25252Fen%25252Fcareers%25252Fexperienced-jobs%25252Fdescription.html%25253Fwdjobreqid%25253D11864WD%252526wdcountry%25253DIND%252526%2526ot%253DA',
    "referer": "https://www.pwc.in/careers/experienced-jobs/results.html?wdcountry=IND&wdjobsite=Global_Experienced_Careers",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
}

params = {
    "wdcountry": "IND",
    "wdjobsite": "Global_Experienced_Careers",
}


#
def make_request(url):
    resp = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    return resp


def get_all_jobs() -> list:

    resp = requests.get(
        base_url,
        params=params,
        cookies=cookies,
        headers=headers,
    )

    # print(resp.status_code)

    # Regex to extract the JSON data
    json_data = re.search(r"var\sjsondata = \[[^\]]*]", resp.text)
    # Remove the JavaScript variable name
    json_data = json_data.group(0).replace("var jsondata = ", "")
    # Convert the JSON data to a Python dictionary
    data = json.loads(json_data)
    # Print the data
    # print(data[0])
    return data


def get_job_details(jobtitle, jobid) -> dict:

    new_params = params
    new_params["wdjobtitle"] = jobtitle
    new_params["wdjobreqid"] = jobid

    # print(params)

    try:
        resp = requests.get(
            jd_url,
            params=new_params,
            cookies=cookies,
            headers=headers,
        )
        # print(resp.status_code)

        # Regex to extract the JSON data
        json_data = re.search(r"var\sjsondata = \{[^}]*\}", resp.text)

        # Remove the JavaScript variable name
        json_data = json_data.group(0).replace("var jsondata = ", "")
        # Convert the JSON data to a Python dictionary
        data = json.loads(json_data)
    except Exception as e:
        # print("Job details not found for:", jobtitle, jobid)
        data = get_job_details(jobtitle, jobid)
    # print(data)
    # Print the data
    return data


def update_job(job):
    job.update(get_job_details(job["title"], job["jobreqid"]))


def to_json(data):

    new_json = {}
    new_json["Company"] = "PwC"
    new_json["Career Page"] = base_url
    new_json["data"] = data

    with open(OUTPUT_FILE, "w") as f:
        json.dump(new_json, f, indent=4)


def main():

    # update all_jobs with job details using threads
    print("Starting PWC Scraper")

    print("Getting all jobs")
    all_jobs = get_all_jobs()

    print("Getting job details")
    Threads = []
    for job in all_jobs:
        t = Thread(target=update_job, args=(job,))
        Threads.append(t)
    for t in Threads:
        t.start()
    for t in Threads:
        t.join()

    # for job in all_jobs[::-1]:
    #     print(job)
    #     break

    print("Writing to JSON")
    to_json(all_jobs)

    print("Done")


if __name__ == "__main__":
    main()
