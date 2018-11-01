import smtplib

def send_email(data):
    TO = "input receiver's email"
    SUBJECT = 'Shooting News in Toronto'


    # Gmail Sign In
    gmail_sender = 'your email'
    gmail_passwd = 'password'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # go th this website : https://myaccount.google.com/lesssecureapps to allow this program to login 
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', data])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error')

    server.quit()
