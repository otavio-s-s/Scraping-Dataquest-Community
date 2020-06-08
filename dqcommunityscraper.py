from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import smtplib
from time import sleep


def send_email(subject, msg):
    try:
        mail_from = 'your email as string'
        password = 'Your password as string'
        mail_to = 'The email address that will receive the email as string'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(mail_from, password)
        message = f'Subject: {subject}\n\n{msg}'
        server.sendmail(mail_from, mail_to, message)
        server.quit()
        print('Email successfully sent!')
    except:
        print('Failed to send email.')


while True:
    my_url = 'https://community.dataquest.io/c/qa/44'
    option = Options()
    option.headless = True
    driver = webdriver.Chrome(options=option)
    driver.get(my_url)

    tables = pd.read_html(driver.page_source)
    table = tables[0]

    table = table.iloc[1:10, [0, 2, 5]]
    table['time'] = table['Activity'].str[-1]
    table['Activity'] = table['Activity'].str[:-1].astype(int)

    new_topics = table[(table['time'] == 'm') & (table['Activity'] <= 10) & (table['Replies'] == 0)]
    new_topics = new_topics.reset_index(drop=True)

    num_new = new_topics.shape[0]

    if num_new > 0:
        subject = f'{num_new} new topics!'
        msg = f'New topics: \n {new_topics}\n\n {my_url}'
        send_email(subject, msg)
    else:
        print('No new topics found.')

    sleep(600)
