import csv
from core.models import Company
from accounting.models import Account

with open('scripts/data/Accounts.csv') as fi:
    reader = csv.reader(fi)
    next(reader)
    rows = list(reader)

company = Company.objects.get(pk=1)
account_map = {}

for account_id, account_number, account_name, account_en_name, parent_id in rows:
    #print(account_id, account_number, account_name, account_en_name, parent_id)
    account_map[account_id] = Account.objects.create(
        company=company,
        code=account_number,
        parent=account_map.get(parent_id),
        name=account_name,
        english_name=account_en_name,
        balance=0
    )