# Synthetic Security Ticket Generator

A Python-based tool for generating synthetic security incident tickets with realistic named entities (PERSON, EMAIL, IP, ORG, URL). Designed for testing, training, and benchmarking security automation systems, NLP models, and incident response workflows.

## Features

- **Configurable data generation**: All names, companies, domains, titles, and description templates are externalized in `data/config.json`
- **Rich entity types**: Generates PERSON, EMAIL, IP, ORG, and URL entities
- **Multiple output formats**: CSV, JSON, and semicolon-delimited entity logs
- **Reproducible**: Uses fixed random seed for consistent outputs
- **Customizable**: Easy to extend with additional scenarios, severities, and templates

## Requirements

- Python 3.10 or higher
- pandas library

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd gerador-sintetico
```

2. (Optional) Create and activate a virtual environment:
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install pandas
```

## Usage

Run the generator:
```bash
python gerador.py
```

The script will:
1. Load configuration from `data/config.json`
2. Generate 100 synthetic tickets with associated entities
3. Save outputs to the `out/` directory
4. Display a preview of the first 10 tickets and entity statistics

## Configuration

All data sources and parameters are defined in `data/config.json`:

- **first_names**: List of first names for synthetic persons
- **last_names**: List of last names for synthetic persons
- **companies**: List of company/organization names
- **domains**: List of email/URL domains
- **url_templates**: URL patterns with `{d}` (domain) and `{id}` (ticket ID) placeholders
- **titles**: Incident ticket titles
- **description_templates**: Ticket description templates with placeholders:
  - `{person}` - Full name
  - `{email}` - Email address
  - `{ip}` - IP address
  - `{org}` - Organization name
  - `{url}` - URL
  - `{date}` - Incident date
- **severity_levels**: List of severity classifications (default: `["Low", "Medium", "High", "Critical"]`)
- **date_range**: Start and end dates for random date generation
- **alt_email_probability**: Probability (0.0-1.0) of adding an alternate email to a ticket

### Example Configuration Snippet

```json
{
  "titles": [
    "Suspicious access detected",
    "Phishing reported by user",
    "Anomalous login attempts"
  ],
  "description_templates": [
    "Report received from {person} ({email}) indicating suspicious access to {org} resources. IP observed: {ip}. Details at {url}."
  ],
  "severity_levels": ["Low", "Medium", "High", "Critical"],
  "date_range": {
    "start": "2024-01-01",
    "end": "2025-11-09"
  },
  "alt_email_probability": 0.2
}
```

## Output Files

All outputs are saved to the `out/` directory:

### 1. `tickets_sinteticos.csv`
Main dataset in CSV format with columns:
- `ticket_id`: Unique ticket identifier (e.g., TCKT-001)
- `title`: Incident title
- `date`: Incident date (ISO format)
- `severity`: Severity level
- `description`: Full incident description with embedded entities
- `entities`: JSON string containing all entities found in the ticket
- `entity_count`: Number of entities in the ticket

### 2. `tickets_entities.json`
Complete ticket data in JSON format with full entity annotations per ticket.

### 3. `tickets_summary.json`
Statistical summary:
```json
{
  "PERSON": 100,
  "EMAIL": 120,
  "IP": 100,
  "ORG": 100,
  "URL": 100,
  "TOTAL_TICKETS": 100,
  "TOTAL_ENTITIES": 520
}
```

### 4. `entities_semicolon.log`
Detailed entity log in semicolon-delimited format:
```
ticket_id;type;value
TCKT-001;PERSON;Lucas Silva
TCKT-001;EMAIL;lucas.silva17@example.com
TCKT-001;IP;192.168.1.45
```

This format is ideal for:
- Secondary counting and validation
- External entity extraction pipelines
- Training data preparation for NER models

## Example Output

```
Resumo das entidades geradas:
 - PERSON: 100
 - EMAIL: 120
 - IP: 100
 - ORG: 100
 - URL: 100
Total de tickets: 100
Total de entidades: 520

Arquivos gerados:
- CSV: c:\...\out\tickets_sinteticos.csv
- JSON com anotações por ticket: c:\...\out\tickets_entities.json
- Resumo (JSON): c:\...\out\tickets_summary.json
- Log de entidades (;): c:\...\out\entities_semicolon.log
```

## Customization

### Adding More Data

Edit `data/config.json` to add:
- New names, companies, or domains
- Additional incident scenarios in `titles`
- New description templates with varied patterns
- Custom severity levels

### Changing Output Volume

Modify line 76 in `gerador.py`:
```python
for i in range(1, 101):  # Change 101 to generate different number of tickets
```

### Adjusting Randomness

Change the seed on line 19 in `gerador.py`:
```python
random.seed(42)  # Use different seed for different outputs
```

## Use Cases

- **Training NER models**: Use entity logs for named entity recognition
- **Testing SIEM systems**: Import synthetic tickets into security platforms
- **Incident response drills**: Generate realistic test scenarios
- **Data pipeline validation**: Verify ETL and analysis workflows
- **Privacy-safe datasets**: Share synthetic data without PII concerns

## Project Structure

```
gerador-sintetico/
├── data/
│   └── config.json          # Configuration and data sources
├── out/                      # Generated outputs (created on first run)
│   ├── tickets_sinteticos.csv
│   ├── tickets_entities.json
│   ├── tickets_summary.json
│   └── entities_semicolon.log
├── gerador.py               # Main generator script
└── README.md                # This file
```

## Contributing

To add new incident scenarios:
1. Add titles to `titles` array in `config.json`
2. Add corresponding description templates to `description_templates`
3. Ensure templates use available placeholders: `{person}`, `{email}`, `{ip}`, `{org}`, `{url}`, `{date}`

## License

This project is provided as-is for research and educational purposes.

## Notes

- The generator uses a fixed random seed (42) for reproducibility
- IP addresses are randomly generated (not real)
- All names, companies, and domains are fictional
- Email addresses are synthetic combinations
- The `caas_jupyter_tools` import has a fallback for non-Jupyter environments
