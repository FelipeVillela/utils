import datetime as dt
import pytz
import jwt
import smtplib
import email.message
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEVEIVER_EMAIL = os.getenv('RECEVEIVER_EMAIL')
SENDER_PASS = os.getenv('SENDER_PASS')

def encode_jwt(payload, secret='secret', expires_in=3600):
    payload['exp'] = dt.datetime.now(pytz.timezone('America/Sao_Paulo')) + dt.timedelta(minutes=expires_in)
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(token, secret='secret', options={'require': ['exp'],'verify_exp': True}):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'], options=options)
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError('Token expired')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')

def send_email(subject, body):
    try:
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEVEIVER_EMAIL
        password = SENDER_PASS
        msg.add_header('Content-Type', 'text/html')

        msg.set_payload(body)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        
        print('Email enviado')
        return 0
    
    except Exception as e:
        print(f"Ocorreu um erro com a exceção {e}")
        return 1

def mask_cpf(cpf):
    # A Partir de um cpf que contenha somente números, retorna formatado
    mask_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return mask_cpf

def mask_phone(phone):
    # Função que retorna um número de telefone que contém somente números 
    # no formato (XX) XXXX-XXXX
    #
    if len(phone) == 11:
        mask_phone = f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"

    elif len(phone) == 10:
        mask_phone = f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"

    else:
        mask_phone = phone

    return mask_phone

def format_separators(value, decimal_separator=',', thousand_separator='.'):
    # Função que retorna uma string de um número formatado com separador de milhar e decimal
    if type(value) == float:
        # Troca o decimal separator padrão para D e o thousand separator padrão para T
        value = ('{:,.2f}'.format(float(value))).replace('.', 'D').replace(',', 'T')
        value = value.replace('D', decimal_separator).replace('T', thousand_separator)
    elif type(value) == int:
        value = f'{value:,}'.replace(',', '.')
    
    return value

def format_currency(value, currency='R$', value_format='cents', decimal_separator=',', thousand_separator='.'):
    # Função para formatar uma moeda a partir do seu valor em centavos
    value = value if value_format != 'cents' else value/100
    formated_value = format_separators(float(value), decimal_separator, thousand_separator)
    return f'{currency} {formated_value}'

