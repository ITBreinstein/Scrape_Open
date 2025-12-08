Deze scraper schrijft automatisch nieuwe vacatures (LinkedIn & Indeed) voor het vakgebied Data naar de Supabase database. <br>
Het wordt gerund met Docker via Google Cloud Run Jobs: https://console.cloud.google.com/run/jobs/details/europe-west1/scrape-open-job/executions?authuser=0&hl=nl&inv=1&invt=Ab2eJA&project=potent-terminal-465211-d3
<br>
<br>
Nadat je code heb aangepast, navigeer binnen de Google Cloud Shell Terminal naar deze repo, pull de nieuwe code en run het volgende (zorg dat Docker runt): <br>
1. Image bouwen: <br>
   ```gcloud builds submit --tag gcr.io/potent-terminal-465211-d3/scrape-open ``` <br>
2. Aanpassingen updaten: <br>
   ```gcloud run jobs create scrape-open-job \ ```
   ```--image gcr.io/potent-terminal-465211-d3/scrape-open \ ```
   ```--region europe-west1 \ ```
   ```--memory 1Gi ```
3. Run de nieuwe job: <br>
   ```gcloud run jobs execute scrape-open-job --region europe-west1 ```
