# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from notification import send_emails_smtp

send_emails_smtp(['t@t.com'], "hello", "Thanks very much, 非常感谢！")
