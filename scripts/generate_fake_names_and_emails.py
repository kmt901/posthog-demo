from faker import Faker
import csv
import random
fake = Faker()

last_names = [fake.unique.last_name() for i in range(100)]

with open('500_names_and_emails.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['last_name','family_id','email','ip','plan','is_adult'])
    for i in range(500):
        first_name = fake.first_name()
        last_name = random.choice(last_names)
        domain = fake.safe_domain_name()
        ip = fake.ipv4() 
        plan = random.choice(['Free', 'Premium', 'Max-imal']) 
        is_adult = random.choice(['Yes','No'])

        email = first_name.lower() + '.' + last_name.lower() + '@' + domain
        csvwriter.writerow([last_name,str(last_names.index(last_name)),email, ip, plan, is_adult])
