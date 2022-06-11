import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
from pathlib import Path
from faker import Faker

try:
    initial_path = Path('resources/initial-data')
    initial_path.mkdir(parents=True)
except OSError as e:
    print('Directory exists')

try:
    sample_path = Path('resources/sample-data')
    sample_path.mkdir(parents=True)
except OSError as e:
    print('Directory exists')

### -------------------- Constants -------------------- ###
fake = Faker()
entity_num = 25
user_num_low = 5
user_num_high = 5

### -------------------- Functions -------------------- ###
def gen_date(min_date):
    if min_date != None:
        return fake.date_time_between(start_date= datetime.strptime(min_date, '%Y/%m/%d %H:%M') + 
            relativedelta(months = 1), end_date=datetime(2099, 12, 1,23,59,59)).strftime('%Y/%m/%d %H:%M')
    else:
        return fake.date_time().strftime('%Y/%m/%d %H:%M')

def gen_date_recent():
    return fake.date_time_between(start_date= datetime.now() - relativedelta(months = 1), end_date=datetime.now()).strftime('%Y/%m/%d %H:%M')

def gen_100():
    return fake.text(max_nb_chars=100).replace('\n', ' ')

def gen_255():
    return fake.text(max_nb_chars=255).replace('\n', ' ')

def gen_bool():
    return fake.pybool()

def gen_auth():
    return fake.name()

def gen_chance(chance):
    rand = random.random()
    if(rand > chance):
        return True
    else:
        return False
    
def gen_url():
    if(gen_chance(0.2)):
        return fake.url()
    else:
        return 'null'

def gen_email():
    if(gen_chance(0.2)):
            return fake.email()
    else:
        return 'null'

def gen_code(codes):
    if(gen_chance(0.2)):
        code = fake.bothify(text='###')
        while(code in codes):
            code = fake.bothify(text='###')
        return code
    else:
        code = fake.bothify(text='###-?')
        while(code in codes):
            code = fake.bothify(text='###-?')
        return code.upper()

def gen_money():
    return fake.word(ext_word_list=['EUR','USD','CAD']) + ' ' + str(round(random.uniform(1,999999),2))

def gen_identity():
    # UserIdentity{name: 'John', surname: 'Doe', email: 'john.doe@acme.com'}
    return "UserIdentity{name: '" + fake.first_name() + "', surname: '" + fake.last_name() + "', email: '" + fake.email() + "'}"

def gen_type(word_list):
    return fake.words(nb=1, ext_word_list=word_list)[0]
    

### -------------------- Announcement -------------------- ###
def gen_announcements():
    fpath = (sample_path / 'announcement').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','creationMoment','title','body','critical','link']
        write.writerow(header)
        # Add test data
        for i in range(entity_num):
            row = []
            row.append('announcement-' + str(i+1))
            row.append(gen_date_recent())
            row.append(gen_100())
            row.append(gen_255())
            row.append(gen_bool())
            row.append(gen_url())

            write.writerow(row)

### -------------------- Chirp -------------------- ###
def gen_chirps():
    fpath = (sample_path / 'chirp').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','moment','title','author','body','mail']
        write.writerow(header)
        for i in range(entity_num):
            row = []
            row.append('chirp-' + str(i+1))
            row.append(gen_date_recent())
            row.append(gen_100())
            row.append(gen_100())
            row.append(gen_255())
            row.append(gen_email())

            write.writerow(row)

### -------------------- Items -------------------- ###
def gen_items():
    fpath = (sample_path / 'item').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','name','code','technology','description','price','item-type','link','key:inventor']
        write.writerow(header)
        codes = []
        for i in range(entity_num):
            row = []
            row.append('item-' + str(i+1))
            row.append(gen_100())

            code = gen_code(codes)
            codes.append(code)
            row.append('ITM-' + str(code))

            row.append(gen_100())
            row.append(gen_255())
            row.append(gen_money())
            row.append(gen_type(['COMPONENT','TOOL']))
            row.append(gen_url())
            row.append('inventor-' + str(random.randint(2,user_num_low + user_num_high + 1)))

            write.writerow(row)

### -------------------- Patronage -------------------- ###
def gen_patronage():
    fpath = (sample_path / 'patronage').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','status','code','legislation','budget','creation-date','start-date','finish-date','link','key:inventor','key:patron']
        write.writerow(header)

        codes = []
        for i in range(entity_num):
            row = []
            row.append('patronage-' + str(i+1))
            row.append(gen_type(['Accepted','Denied','Proposed']))
            
            code = gen_code(codes)
            codes.append(code)
            row.append('PTG-' + code)

            row.append(gen_255())
            row.append(gen_money())

            creation_date = gen_date(None)
            start_date = gen_date(creation_date)
            end_date = gen_date(start_date)
            row.append(creation_date)
            row.append(start_date)
            row.append(end_date)

            row.append(gen_url())
            row.append('inventor-' + str(random.randint(2,user_num_low + user_num_high + 1)))
            row.append('patron-' + str(random.randint(2,user_num_low + user_num_high + 1)))

            write.writerow(row)

### -------------------- Patronage Report -------------------- ###
def gen_patronage_report():
    fpath = (sample_path / 'patronage-report').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','creation','link','memorandum','key:patronage']
        write.writerow(header)

        for i in range(entity_num):
            row = []
            row.append('patronage-report-' + str(i+1))

            # ! TODO Date must be after the patronage that is linked
            row.append(gen_date(None))
            row.append(gen_url())
            row.append(gen_255())
            row.append('patronage-' + str(random.randint(1,entity_num)))

            write.writerow(row)

### -------------------- Toolkit -------------------- ###
def gen_toolkits():
    fpath = (sample_path / 'toolkit').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','code','draft-mode','title','description','assembly-notes','link','key:inventor']
        write.writerow(header)

        codes = []
        for i in range(entity_num):
            row = []
            row.append('toolkit-' + str(i+1))
            
            code = gen_code(codes)
            codes.append(code)
            row.append('TLK-' + code)

            row.append(gen_chance(0.9))
            row.append(gen_100())
            row.append(gen_255())
            row.append(gen_255())

            row.append(gen_url())
            row.append('inventor-' + str(random.randint(1,user_num_low + user_num_high)))

            write.writerow(row)

### -------------------- Quantity -------------------- ###
def gen_quantity():
    fpath = (sample_path / 'quantity').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','key:toolkit','key:item','item-quantity']
        write.writerow(header)

        codes = []
        for i in range(entity_num):
            row = []
            row.append('quantity-' + str(i+1))

            row.append('toolkit-' + str(random.randint(1,user_num_low + user_num_high)))
            row.append('item-' + str(random.randint(1,user_num_low + user_num_high)))
            row.append(random.randint(1,25))

            write.writerow(row)

### -------------------- Users -------------------- ###
def gen_users():
    fpath = (initial_path / 'user-account').with_suffix('.csv')
    with fpath.open('w', newline='', encoding='UTF-8') as f:
        write = csv.writer(f)
        header = ['key','enabled','identity','password','username']
        write.writerow(header)
        # --- Anonymous --- #
        row = []
        row.append('user-account-anonymous-1')
        row.append(gen_bool())
        row.append(gen_identity())
        row.append('HIDDEN-PASSWORD')
        row.append('anonymous')

        write.writerow(row)

        fpath_anonymous = (initial_path / 'anonymous').with_suffix('.csv')
        with fpath_anonymous.open('w', newline='', encoding='UTF-8') as f:
            write_anonymous = csv.writer(f)
            header = ['key','key:user-account']
            write_anonymous.writerow(header)
            row = []
            row.append('anonymous-1')
            row.append('user-account-anonymous-1')

            write_anonymous.writerow(row)

        # --- Administrator --- #
        row = []
        row.append('user-account-administrator-1')
        row.append(True)
        row.append(gen_identity())
        row.append('administrator')
        row.append('administrator')
        
        write.writerow(row)

        fpath_admin = (initial_path / 'administrator').with_suffix('.csv')
        with fpath_admin.open('w', newline='', encoding='UTF-8') as f:
            write_admin = csv.writer(f)
            header = ['key','key:user-account']
            write_admin.writerow(header)
            row = []
            row.append('administrator-1')
            row.append('user-account-administrator-1')

            write_admin.writerow(row)

        # --- Inventor --- #
        for i in range(user_num_low):
            row = []
            row.append('user-account-inventor-' + str(i+1))
            row.append(True)
            row.append(gen_identity())
            row.append('inventor' + str(i+1))
            row.append('inventor' + str(i+1))

            write.writerow(row)

        for i in range(user_num_high):
            row = []
            row.append('user-account-inventor-' + str(i+user_num_low+1))
            row.append(gen_bool())
            row.append(gen_identity())
            row.append('inventor' + str(i+user_num_low+1))
            row.append('inventor' + str(i+user_num_low+1))

            write.writerow(row)

        fpath_inventor = (sample_path / 'inventor').with_suffix('.csv')
        with fpath_inventor.open('w', newline='', encoding='UTF-8') as f:
            write_inventor = csv.writer(f)
            header = ['key','key:user-account','company','statement','link']
            write_inventor.writerow(header)

            row = []
            row.append('inventor-1')
            row.append('user-account-administrator-1')
            row.append(fake.company())
            row.append(gen_255())
            row.append(gen_url())
            write_inventor.writerow(row)

            for i in range(user_num_low + user_num_high):
                row = []
                row.append('inventor-' + str(i+2))
                row.append('user-account-inventor-' + str(i+1))
                row.append(fake.company())
                row.append(gen_255())
                row.append(gen_url())

                write_inventor.writerow(row)

        # --- Patron --- #
        for i in range(user_num_low):
            row = []
            row.append('user-account-patron-' + str(i+1))
            row.append(True)
            row.append(gen_identity())
            row.append('patron' + str(i+1))
            row.append('patron' + str(i+1))

            write.writerow(row)

        for i in range(user_num_high):
            row = []
            row.append('user-account-patron-' + str(i+user_num_low+1))
            row.append(gen_bool())
            row.append(gen_identity())
            row.append('patron' + str(i+user_num_low+1))
            row.append('patron' + str(i+user_num_low+1))

            write.writerow(row)

        fpath_patron = (sample_path / 'patron').with_suffix('.csv')
        with fpath_patron.open('w', newline='', encoding='UTF-8') as f:
            write_patron = csv.writer(f)
            header = ['key','key:user-account','company','statement','link']
            write_patron.writerow(header)

            row = []
            row.append('patron-1')
            row.append('user-account-administrator-1')
            row.append(fake.company())
            row.append(gen_255())
            row.append(gen_url())
            write_patron.writerow(row)

            for i in range(user_num_low+user_num_high):
                row = []
                row.append('patron-' + str(i+2))
                row.append('user-account-patron-' + str(i+1))
                row.append(fake.company())
                row.append(gen_255())
                row.append(gen_url())

                write_patron.writerow(row)

        # --- Consumer --- #
        for i in range(user_num_low):
            row = []
            row.append('user-account-consumer-' + str(i+1))
            row.append(True)
            row.append(gen_identity())
            row.append('consumer' + str(i+1))
            row.append('consumer' + str(i+1))

            write.writerow(row)

        for i in range(user_num_high):
            row = []
            row.append('user-account-consumer-' + str(i+user_num_low+1))
            row.append(gen_bool())
            row.append(gen_identity())
            row.append('consumer' + str(i+user_num_low+1))
            row.append('consumer' + str(i+user_num_low+1))

            write.writerow(row)

        fpath_consumer = (sample_path / 'consumer').with_suffix('.csv')
        with fpath_consumer.open('w', newline='', encoding='UTF-8') as f:
            write_consumer = csv.writer(f)
            header = ['key','key:user-account','company','sector']
            write_consumer.writerow(header)\

            row = []
            row.append('consumer-1')
            row.append('user-account-administrator-1')
            row.append(fake.company())
            row.append(fake.bs())
            write_consumer.writerow(row)

            for i in range(user_num_low+user_num_high):
                row = []
                row.append('consumer-' + str(i+2))
                row.append('user-account-consumer-' + str(i+1))
                row.append(fake.company())
                row.append(fake.bs())

                write_consumer.writerow(row)

        # --- Provider --- #
        for i in range(user_num_low):
            row = []
            row.append('user-account-provider-' + str(i+1))
            row.append(True)
            row.append(gen_identity())
            row.append('provider' + str(i+1))
            row.append('provider' + str(i+1))

            write.writerow(row)

        for i in range(user_num_high):
            row = []
            row.append('user-account-provider-' + str(i+user_num_low+1))
            row.append(gen_bool())
            row.append(gen_identity())
            row.append('provider' + str(i+user_num_low+1))
            row.append('provider' + str(i+user_num_low+1))

            write.writerow(row)

        fpath_provider = (sample_path / 'provider').with_suffix('.csv')
        with fpath_provider.open('w', newline='', encoding='UTF-8') as f:
            write_provider = csv.writer(f)
            header = ['key','key:user-account','company','sector']
            write_provider.writerow(header)\

            row = []
            row.append('provider-1')
            row.append('user-account-administrator-1')
            row.append(fake.company())
            row.append(fake.bs())
            write_provider.writerow(row)

            for i in range(user_num_low+user_num_high):
                row = []
                row.append('provider-' + str(i+2))
                row.append('user-account-provider-' + str(i+1))
                row.append(fake.company())
                row.append(fake.bs())

                write_provider.writerow(row)

### -------------------- Execution -------------------- ###
#gen_announcements()
#gen_chirps()
#gen_items()
#gen_patronage()
#gen_toolkits()
gen_quantity()
#gen_patronage_report()
#gen_users()