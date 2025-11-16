"""
Gerar 100 tickets sintéticos com entidades (PERSON, EMAIL, IP, ORG, URL).

Agora, os títulos, templates e listas (nomes, empresas, domínios, urls) são lidos de
um arquivo de configuração externo em JSON: data/config.json.
"""
import random, json, os, csv, datetime
import pandas as pd
try:
    from caas_jupyter_tools import display_dataframe_to_user
except Exception:  # fallback quando não disponível
    def display_dataframe_to_user(title: str, df):
        print(f"{title} (preview)")
        try:
            print(df.head(10).to_string(index=False))
        except Exception:
            print(df)

random.seed(42)

# Caminho do arquivo de configuração externo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "data", "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

# Listas carregadas do arquivo
first_names = cfg.get("first_names", [])
last_names = cfg.get("last_names", [])
companies = cfg.get("companies", [])
domains = cfg.get("domains", [])
url_templates = cfg.get("url_templates", [])
titles = cfg.get("titles", [])
templates = cfg.get("description_templates", [])
severity_levels = cfg.get("severity_levels", ["Low","Medium","High","Critical"])
date_range = cfg.get("date_range", {"start":"2024-01-01","end":"2025-11-09"})
alt_email_probability = float(cfg.get("alt_email_probability", 0.2))

# Helpers
def rnd_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def rnd_email(name):
    user = name.lower().replace(" ",".") + str(random.randint(1,99))
    domain = random.choice(domains)
    return f"{user}@{domain}"

def rnd_ip():
    return ".".join(str(random.randint(1,254)) for _ in range(4))

def rnd_company():
    return random.choice(companies)

def rnd_url(ticket_id):
    tmpl = random.choice(url_templates)
    d = random.choice(domains)
    return tmpl.format(d=d, id=ticket_id)

def rnd_date():
    try:
        y1,m1,d1 = map(int, date_range["start"].split("-"))
        y2,m2,d2 = map(int, date_range["end"].split("-"))
        start = datetime.date(y1,m1,d1).toordinal()
        end = datetime.date(y2,m2,d2).toordinal()
    except Exception:
        start = datetime.date(2024,1,1).toordinal()
        end = datetime.date(2025,11,9).toordinal()
    return datetime.date.fromordinal(random.randint(start,end)).isoformat()

tickets = []
all_entities = []

for i in range(1,101):
    ticket_id = f"TCKT-{i:03d}"
    person = rnd_name()
    email = rnd_email(person)
    ip = rnd_ip()
    org = rnd_company()
    url = rnd_url(i)
    date = rnd_date()
    template = random.choice(templates)
    # Como removemos PHONE, garantimos que o placeholder {phone} não apareça em templates novos
    desc = template.format(person=person, email=email, ip=ip, org=org, url=url, date=date)
    title = random.choice(titles)
    severity = random.choice(severity_levels)
    
    # Identificar entidades usadas neste ticket
    entities = []
    entities.append({"type":"PERSON","value":person})
    entities.append({"type":"EMAIL","value":email})
    entities.append({"type":"IP","value":ip})
    entities.append({"type":"ORG","value":org})
    entities.append({"type":"URL","value":url})
    # Possibilidade de incluir adicional email alternativo
    if random.random() < alt_email_probability:
        alt = rnd_email(person)
        entities.append({"type":"EMAIL","value":alt})
        desc += f" Email alternativo: {alt}."
    tickets.append({
        "ticket_id": ticket_id,
        "title": title,
        "date": date,
        "severity": severity,
        "description": desc,
        "entities": json.dumps(entities, ensure_ascii=False),
        "entity_count": len(entities)
    })
    for e in entities:
        # Guardar log detalhado por entidade (inclui ticket_id)
        all_entities.append({
            "ticket_id": ticket_id,
            "type": e["type"],
            "value": e["value"],
        })

# Summary counts por tipo
from collections import Counter, defaultdict
counter = Counter([e["type"] for e in all_entities])
summary = dict(counter)
summary["TOTAL_TICKETS"] = len(tickets)
summary["TOTAL_ENTITIES"] = sum(counter.values())

# Salvar CSV e JSON de anotações
# Ajuste do diretório de saída para Windows: cria pasta local ./out
out_dir = os.path.join(BASE_DIR, "out")
os.makedirs(out_dir, exist_ok=True)
csv_path = os.path.join(out_dir, "tickets_sinteticos.csv")
json_path = os.path.join(out_dir, "tickets_entities.json")
summary_path = os.path.join(out_dir, "tickets_summary.json")
entities_log_path = os.path.join(out_dir, "entities_semicolon.log")

df = pd.DataFrame(tickets)
df.to_csv(csv_path, index=False, quoting=csv.QUOTE_MINIMAL)
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(tickets, f, ensure_ascii=False, indent=2)
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

# Gravar log de entidades separadas por ponto e vírgula
with open(entities_log_path, "w", encoding="utf-8") as f:
    f.write("ticket_id;type;value\n")
    for e in all_entities:
        value = str(e["value"]).replace(";", ",")
        f.write(f"{e['ticket_id']};{e['type']};{value}\n")

# Mostrar um preview para o usuário (primeiras 10 linhas)
display_dataframe_to_user("Preview - 10 primeiros tickets", df.head(10))

# Exibir resumo
print("Resumo das entidades geradas:")
for k,v in counter.items():
    print(f" - {k}: {v}")
print(f"Total de tickets: {summary['TOTAL_TICKETS']}")
print(f"Total de entidades: {summary['TOTAL_ENTITIES']}")
print("\nArquivos gerados:")
print(f"- CSV: {csv_path}")
print(f"- JSON com anotações por ticket: {json_path}")
print(f"- Resumo (JSON): {summary_path}")
print(f"- Log de entidades (;): {entities_log_path}")
