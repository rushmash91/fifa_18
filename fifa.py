import dryscrape
import bs4 as bs
import pandas as pd
from mail import send_mail
from sensitive import *


def main():
    url = 'https://us.soccerway.com/teams/rankings/fifa/?ICID=TN_03_05_01'

    sess = dryscrape.Session()
    sess.visit(url)
    source = sess.body()

    soup = bs.BeautifulSoup(source, 'lxml')

    table = soup.table
    trs = table.find_all('tr')

    data = []

    for tr in trs:
        td = tr.find_all('td')
        row = [i.text for i in td]
        data.append(row)

    data.pop(0)

    for d in data:
        d.pop(3)

    rank = 'Not Found'

    for d in data:
        if d[1] == 'India':
            rank = d[0]

    df = pd.DataFrame(data)

    df.loc[-1] = ['Rank', 'Country', 'Points', 'Change in Position']
    df.index = df.index + 1
    df.sort_index(inplace=True)

    df = df.to_string(index=False)

    body = "India's Current Fifa Ranking is " + str(rank) + "\n\n\n\n\n\n" + "                            The List " \
                                                                             "    " +"\n\n" + "" + str(df)

    body = body.encode('ascii', 'ignore').decode('ascii')

    send_mail(me, 'Fifa Ranking India', body)


if __name__ == '__main__':
    main()