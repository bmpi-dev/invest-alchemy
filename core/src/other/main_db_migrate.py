# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from pyliquibase import Pyliquibase
from multiprocessing import Process

def do_db_migration():
    liquibase = Pyliquibase(defaultsFile="db/liquibase.properties")
    liquibase.update()

print('\nstart migrate db in a new process...\n')
p = Process(target=do_db_migration, args=())
p.start()
p.join(timeout=60)

if p.is_alive():
    print('do db migration timeout error...\n')
    p.terminate()
else:
    print('done db migration')