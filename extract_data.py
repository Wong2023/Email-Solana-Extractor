import re
import pandas as pd

input_file = "input.txt"
output_file = "output.xlsx"

# Регулярки
email_pass_pattern = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([^\s]+)')
solana_pattern = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
proxy_pattern = re.compile(r'^(socks5?://|http://|https://)')  # для исключения строк прокси

emails = []
passwords = []
sol_wallets = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        # Пропускаем строки с прокси
        if proxy_pattern.match(line):
            continue

        # Ищем email:password пары
        match = email_pass_pattern.search(line)
        if match:
            emails.append(match.group(1))
            passwords.append(match.group(2))
        else:
            # Ищем кошелек Solana
            wallet_match = solana_pattern.search(line)
            if wallet_match:
                sol_wallets.append(wallet_match.group(0))

# Приводим списки к одинаковой длине
max_len = max(len(emails), len(passwords), len(sol_wallets))
data = {
    "Emails": emails + [""]*(max_len - len(emails)),
    "Пароли": passwords + [""]*(max_len - len(passwords)),
    "Solana кошельки": sol_wallets + [""]*(max_len - len(sol_wallets)),
}

df = pd.DataFrame(data)
df.to_excel(output_file, index=False)
print(f"Файл '{output_file}' создан!")
