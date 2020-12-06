import smtplib
from email.mime.text import MIMEText # enables python to send mail in html or plaintext format

def send_mail(customer, driver, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '160336b4ed58d5'
    password = 'a7240986fee8ea'
    message = f"<h3>Grab Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Driver: {driver}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = "Grab Feedback Submission"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # function to send the mail
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())