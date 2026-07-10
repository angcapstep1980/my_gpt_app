# Configurazione e avvio dell'applicazione

## Configurazione delle variabili d'ambiente

Per il corretto funzionamento dell'applicazione è necessario creare un file `.env` **allo stesso livello del file `docker-compose.yml`**.

Il file `.env` deve contenere e valorizzare le seguenti variabili d'ambiente:

```env
DB_PROTOCOL=
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
```

Assicurarsi che tutte le variabili siano correttamente configurate con i valori relativi all'ambiente di esecuzione prima di avviare l'applicazione.

> **Nota:** il file `.env` contiene informazioni sensibili (come credenziali del database e chiavi API). Assicurarsi di non versionarlo all'interno del repository Git. È consigliato aggiungerlo al file `.gitignore`.

---

## Avvio dell'applicazione

Dopo aver configurato il file `.env`, è possibile avviare l'applicazione tramite Docker Compose.

Dalla directory contenente il file `docker-compose.yml`, eseguire:

```bash
docker-compose up -d
```

L'opzione `-d` permette di avviare i container in modalità **detached**, lasciando l'applicazione in esecuzione in background.

---

## Verifica dello stato dell'applicazione

Per verificare lo stato dei container avviati:

```bash
docker-compose ps
```

Il comando permette di controllare quali servizi sono attivi e il relativo stato di esecuzione.

---

## Visualizzazione dei log

Per visualizzare i log generati dai container:

```bash
docker-compose logs
```

Per seguire i log in tempo reale:

```bash
docker-compose logs -f
```

Per visualizzare i log di uno specifico servizio:

```bash
docker-compose logs -f <nome_servizio>
```

Sostituire `<nome_servizio>` con il nome del container definito nel file `docker-compose.yml`.

---

## Arresto dell'applicazione

Per arrestare l'applicazione e fermare i container:

```bash
docker-compose down
```

Questo comando arresta e rimuove i container creati da Docker Compose, mantenendo comunque le immagini e i volumi presenti.

---

## Riavvio dell'applicazione

Per riavviare l'applicazione dopo eventuali modifiche alla configurazione dei file `.env` o il file `docker-compose.yml`, 
è necessario ricreare i container affinché le nuove configurazioni vengano applicate:

```bash
docker-compose down
docker-compose up -d
```

---

## Aggiornamento della configurazione

Se sono state modificate le immagini Docker o il codice che richiede una nuova build, utilizzare:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```