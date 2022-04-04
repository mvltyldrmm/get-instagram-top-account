import pandas
import requests
import json
import re
from bs4 import BeautifulSoup
from log import logger

logger = logger.return_logger()


def indexes_accounts_get(all_data, i, j, logger):

    try:
        url = f"https://www.instagram.com/directory/profiles/{i}-{j}"
        print("REQUEST URL : ", url)
        response = requests.get(url)
        html_icerigi = response.content
        soup = BeautifulSoup(html_icerigi, "html.parser")

        script_tag = soup.find(
            'script', text=re.compile('window\._sharedData'))
        shared_data = script_tag.string.partition('=')[-1].strip(' ;')

        page_top_account = (json.loads(shared_data)[
                            'entry_data']['ProfilesDirectoryPage'][0]['profile_data']['profile_list'])

        not_list = page_top_account.replace('[', '').replace(']', '')

        list = not_list.split(',')

        for i in list:
            i = i.replace('"', '')
            if i not in all_data:
                all_data.append(i)

        logger.info("Continues..")

        return all_data
    except:
        logger.error("URL REQUEST ERR. CONTINUES..")
        return all_data


i, j, list_data = 0, 0, list()

while(True):

    j += 1
    if j % 15 == 0:
        i += 1
        j = 0

    list_data = indexes_accounts_get(list_data, i, j, logger)

    if i > 0 and j >= 1:
        break  # 0-1,0-2..0-14,1-0,1-1,...1-14,2-1,......20-14

df = pandas.DataFrame(data={"username": list_data})

df.to_csv(f'{input("CSV NAME :")}.csv', sep=',', index=False)
