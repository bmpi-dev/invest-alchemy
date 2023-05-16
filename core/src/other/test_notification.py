# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from notification import send_email_mailgun, send_email_smtp

# send_email_mailgun('test@test.com', "Hello world", "This is a test email")
send_email_smtp('test@test.com', "测试测试", "你好👋")