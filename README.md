Deze scraper schrijft automatisch nieuwe vacatures (LinkedIn & Indeed) voor het vakgebied Data naar de Supabase database. <br>
Het wordt gerund met Docker via Google Cloud Run Jobs: https://console.cloud.google.com/run/jobs/details/europe-west1/scrape-open-job/executions?authuser=0&hl=nl&inv=1&invt=Ab2eJA&project=potent-terminal-465211-d3
<br>
De API-key van de database staat in Google Cloud, te vinden via de bovenstaande link. Ga dan naar View & edit job configuration > Bij Edit container naar Variables & Secrets, en daar vind je ```key_supa```
<br>
Deze wordt vervolgens aangeroepen in scrape_open_core.py: ```SUPABASE_KEY = os.getenv("key_supa")```
<br>
<br>
Nadat je code heb aangepast, navigeer binnen de Google Cloud Shell Terminal naar deze repo, pull de nieuwe code en run het volgende (zorg dat Docker runt): <br>
1. Image bouwen: <br>
   ```gcloud builds submit --tag gcr.io/potent-terminal-465211-d3/scrape-open ``` <br>
2. Aanpassingen updaten: <br>
   ```gcloud run jobs create scrape-open-job \ ```<br>
   ```--image gcr.io/potent-terminal-465211-d3/scrape-open \ ```<br>
   ```--region europe-west1 \ ```<br>
   ```--memory 1Gi ```<br>
3. Run de nieuwe job: <br>
   ```gcloud run jobs execute scrape-open-job --region europe-west1 ```
