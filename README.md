# Tagesthemen

Fork von https://github.com/johl/tagesthemen. Kleine Flask-App, die auf dem ARD-Programm (`https://programm.ard.de/programm/sender?sender=28106&datum=<heute>`) nachschaut, wann die Tagesthemen heute laufen. Per [Serverless Framework](https://www.serverless.com/) deployed in eine AWS Lambda (API Gateway), davor eine CloudFront-Distribution.

## Tech-Stack

- Python (Lambda-Runtime `python3.8`), Flask, requests, BeautifulSoup, pytz
- Serverless Framework v3 mit den Plugins `serverless-wsgi`, `serverless-python-requirements` und `serverless-api-cloudfront`
- AWS: Lambda, API Gateway, CloudFront, Region `eu-central-1`

## Endpunkte

| Pfad     | Antwort                                                                 |
|----------|-------------------------------------------------------------------------|
| `/`      | HTML-Seite (`templates/index.html`) mit der Sendezeit                   |
| `/json`  | JSON mit `when`, `searchTerm` und `url`                                 |
| `/plain` | Nur die Uhrzeit als Text                                                |

Alle Antworten haben `Cache-Control: max-age=300` (5 Minuten).

## Voraussetzungen

- Python 3 und Node.js/npm
- Für das Deployment: AWS-Zugang und ein Serverless-Account (`org`/`app` stehen in `serverless.yml`)

## Setup und lokales Starten

```bash
npm install
pip install -r requirements.txt
python app.py
```

(Dieselben Schritte nutzt `.gitpod.yml`.)

## Deployment

Die Stage ist Pflicht (`dev` oder `prod`), außerdem werden die Parameter `accountId` und `certificateArn` (ACM-Zertifikat für CloudFront) benötigt:

```bash
npx serverless deploy --stage dev  --param="accountId=<AWS_ACCOUNT_ID>" --param="certificateArn=<CERTIFICATE_ARN>"
npx serverless deploy --stage prod --param="accountId=<AWS_ACCOUNT_ID>" --param="certificateArn=<CERTIFICATE_ARN>"
```

Domains laut `serverless.yml`: `tagesthemen.sillium.xyz` (prod) und `dev.tagesthemen.sillium.xyz` (dev). Das Deployment-Bucket (`serverless-deployments-<accountId>`) und das CloudFront-Log-Bucket (`cloudfront-logs-<accountId>`) müssen im Account existieren.

## Projektstruktur

- `app.py` – Flask-App (Scraping des ARD-Programms, Routen)
- `templates/index.html` – HTML-Template für `/`
- `serverless.yml`, `package.json` – Deployment-Konfiguration und Serverless-Plugins
- `requirements.txt` – Python-Abhängigkeiten
- `scriptable/tagesthemen.js` – Scriptable-Widget für iOS, das `/json` abruft
- `shortcut/tagesthemen.shortcut` – iOS-Kurzbefehl
- `.gitpod.yml` – Gitpod-Konfiguration
