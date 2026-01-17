# NetBox Azure Web App Deployment Checklist

## ✅ Configuration Complete
- [x] `configuration.py` configured with:
  - [x] PostgreSQL credentials
  - [x] Redis cache settings (Azure Cache for Redis)
  - [x] SECRET_KEY generated
  - [x] API_TOKEN_PEPPERS set
  - [x] ALLOWED_HOSTS configured

## 📋 Pre-Deployment Steps

### 1. Security - CRITICAL
- [ ] **Store credentials in Azure Key Vault or App Settings** (NOT in configuration.py for production!)
  - Database password
  - Redis password
  - SECRET_KEY
  - Current config.py has these hardcoded - move them to environment variables before pushing to GitHub!

### 2. Environment Variables Setup
Set these in Azure Portal > App Service > Configuration > Application Settings:

```
DJANGO_SETTINGS_MODULE=netbox.settings
WEBSITES_PORT=8000
ALLOWED_HOSTS=netbox-v3-cpasbbgtgkfgd0hw.westeurope-01.azurewebsites.net
CSRF_TRUSTED_ORIGINS=https://netbox-v3-cpasbbgtgkfgd0hw.westeurope-01.azurewebsites.net
REDIS_SCHEME=rediss
```

### 3. Database Preparation
```bash
# Test PostgreSQL connection
psql -h netbox-v3-server.postgres.database.azure.com -U nsssfcnofh -d postgres

# On first deployment, create initial database if needed
# The app will run migrations automatically
```

### 4. Azure Resources Required
- [x] Web App for NetBox UI/API (Linux, Python 3.12-3.14)
- [x] Web App for `netbox-rq` worker (same plan as UI/API)
- [x] PostgreSQL Flexible Server
- [x] Azure Cache for Redis (enable TLS)
- [ ] Storage Account (for media files - optional but recommended)
- [ ] Application Gateway or CDN (optional - for static files)

### 5. Deployment Methods

#### Option A: Docker (Recommended)
```bash
# Build image
docker build -t netbox:latest .

# Push to Azure Container Registry
az acr build --registry myregistry --image netbox:latest .

# Deploy to Web App
az webapp config container set \
  --name netbox-v3-cpasbbgtgkfgd0hw \
  --resource-group mygroup \
  --docker-custom-image-name myregistry.azurecr.io/netbox:latest \
  --docker-registry-server-url https://myregistry.azurecr.io
```

#### Option B: App Service Deployment
```bash
# Clone repo to deployment machine
git clone <your-repo>
cd netbox

# Run migrations
python netbox/manage.py migrate

# Collect static files
python netbox/manage.py collectstatic --noinput

# Deploy via Git/GitHub Actions
git push azure main
```

In App Service, set the web app startup command to bind to the Azure-injected port:

```
gunicorn netbox.wsgi --config ./contrib/gunicorn.py --bind 0.0.0.0:${PORT:-8000}
```

### 6. Post-Deployment Steps
```bash
# SSH into Web App and run:
python /home/site/wwwroot/netbox/manage.py migrate
python /home/site/wwwroot/netbox/manage.py collectstatic --noinput
python /home/site/wwwroot/netbox/manage.py createsuperuser
```

For the RQ worker App Service, set the startup command to:

```
python /home/site/wwwroot/netbox/manage.py rqworker high default low
```

## 🔒 Security Considerations

### Before Going to Production:
1. **NEVER hardcode secrets in configuration.py**
   - Use Azure Key Vault
   - Use environment variables via App Service settings
   - Use Managed Identity for authentication

2. **Update configuration.py to use environment variables:**
```python
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

REDIS = {
    'tasks': {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': int(os.getenv('REDIS_PORT', 6380)),
        'PASSWORD': os.getenv('REDIS_PASSWORD'),
        ...
    },
    ...
}

SECRET_KEY = os.getenv('SECRET_KEY')
API_TOKEN_PEPPERS = {
    1: os.getenv('API_TOKEN_PEPPER_1'),
}
```

3. **Configure HTTPS**
   - Azure Web App provides free SSL certificate
   - Enforce HTTPS in Django settings

4. **Network Security**
   - If using private networks, enable Azure Virtual Network Integration
   - Use Network Security Groups
   - Enable firewall rules on PostgreSQL

## 📊 Files Generated for Deployment
- `startup.sh` - Startup script for Linux App Service
- `web.config` - IIS configuration (if deploying to Windows)
- `Dockerfile` - Docker image definition
- This checklist

## 🚀 Quick Start Commands

### Test locally first:
```bash
cd /workspaces/netbox
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd netbox
python manage.py migrate
python manage.py runserver
```

### Deploy with Docker:
```bash
docker build -t netbox:latest .
docker run -p 8000:8000 \
  -e DJANGO_SETTINGS_MODULE=netbox.settings \
  -e DB_HOST=netbox-v3-server.postgres.database.azure.com \
  -e DB_USER=nsssfcnofh \
  -e DB_PASSWORD='efjpUypk$mxs9I21' \
  -e REDIS_HOST=netbox-v3-cache.redis.cache.windows.net \
  netbox:latest
```

## ⚠️ Known Issues to Address

1. **Static Files in Azure Web App**
   - Web App ephemeral storage (/home/site/wwwroot) is reset on restart
   - Solution: Use Azure Blob Storage OR configure startup.sh to re-collect static files

2. **Media Files**
   - Same issue as static files
   - Solution: Use Azure Blob Storage for persistent media uploads
   - Install: `pip install azure-storage-blob`
   - Configure STORAGES in configuration.py

3. **Private Network Access**
   - If PostgreSQL/Redis on private network: Use VNet Integration (Premium tier)
   - If public: Use firewalls and strong authentication

## 📞 Troubleshooting

Check logs:
```bash
az webapp log tail --name netbox-v3-cpasbbgtgkfgd0hw --resource-group mygroup
```

SSH into container:
```bash
az webapp remote-connection create --resource-group mygroup --name netbox-v3-cpasbbgtgkfgd0hw
```

Check migrations:
```bash
python manage.py showmigrations
python manage.py migrate --plan
```
