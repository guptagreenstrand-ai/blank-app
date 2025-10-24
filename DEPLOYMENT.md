# 🚀 Deployment Guide - Greenstrand Packaging Optimizer

This guide covers various deployment options for the Cutting Plan Optimizer application.

---

## 📦 Deployment Options

### 1. Streamlit Cloud (Recommended for Quick Deploy)

**Free and easy deployment:**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy"

3. **Configuration**
   - App URL: Auto-generated (e.g., `yourapp.streamlit.app`)
   - Python version: 3.8+
   - Resources: Free tier includes 1 GB RAM

**Pros:**
- Free hosting
- Automatic HTTPS
- Easy updates (push to GitHub)
- No server management

**Cons:**
- Limited resources on free tier
- Public by default
- Streamlit branding

---

### 2. Docker Container

**For self-hosting or cloud platforms:**

**Create `Dockerfile`:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (if needed for cairosvg)
# RUN apt-get update && apt-get install -y \
#     libcairo2-dev \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  greenstrand-optimizer:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
    restart: unless-stopped
```

**Deploy:**
```bash
# Build image
docker build -t greenstrand-optimizer .

# Run container
docker run -p 8501:8501 greenstrand-optimizer

# Or use docker-compose
docker-compose up -d
```

---

### 3. AWS EC2

**Steps:**

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.small or larger
   - Security group: Allow inbound on port 8501

2. **SSH and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Install Python
   sudo apt update
   sudo apt install python3-pip python3-venv -y
   
   # Clone repository
   git clone <your-repo-url>
   cd workspace
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run with nohup
   nohup streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

3. **Access**: `http://your-ec2-ip:8501`

**For production:** Use Nginx reverse proxy and SSL certificate.

---

### 4. Google Cloud Platform (Cloud Run)

**Serverless container deployment:**

1. **Prepare Dockerfile** (same as above)

2. **Deploy to Cloud Run**
   ```bash
   # Install gcloud CLI
   # https://cloud.google.com/sdk/docs/install
   
   # Authenticate
   gcloud auth login
   
   # Set project
   gcloud config set project YOUR_PROJECT_ID
   
   # Build and deploy
   gcloud run deploy greenstrand-optimizer \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

3. **Access**: Provided Cloud Run URL

**Pros:**
- Auto-scaling
- Pay-per-use
- Managed infrastructure

---

### 5. Heroku

**Platform-as-a-Service deployment:**

1. **Create `setup.sh`**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

2. **Create `Procfile`**
   ```
   web: sh setup.sh && streamlit run streamlit_app.py
   ```

3. **Deploy**
   ```bash
   # Install Heroku CLI
   # https://devcenter.heroku.com/articles/heroku-cli
   
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

---

### 6. DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Configure:**
   - Type: Web Service
   - Run Command: `streamlit run streamlit_app.py --server.port=8080`
   - HTTP Port: 8080
3. **Deploy**: Automatic on push

---

### 7. Azure Web Apps

**Container deployment:**

1. **Build Docker image** (as above)

2. **Push to Azure Container Registry**
   ```bash
   az acr create --resource-group myResourceGroup --name myRegistry --sku Basic
   az acr login --name myRegistry
   docker tag greenstrand-optimizer myregistry.azurecr.io/greenstrand-optimizer:v1
   docker push myregistry.azurecr.io/greenstrand-optimizer:v1
   ```

3. **Create Web App**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan \
     --name greenstrand-optimizer --deployment-container-image-name \
     myregistry.azurecr.io/greenstrand-optimizer:v1
   ```

---

## 🔒 Production Considerations

### Security

1. **Authentication**
   - Add user authentication (not included in MVP)
   - Consider OAuth, LDAP, or SAML integration

2. **HTTPS**
   - Use reverse proxy (Nginx, Apache)
   - Obtain SSL certificate (Let's Encrypt)

3. **Environment Variables**
   - Store secrets in environment variables
   - Use `.streamlit/secrets.toml` for Streamlit Cloud

### Performance

1. **Caching**
   - Streamlit has built-in caching
   - Use `@st.cache_data` for data processing

2. **Resource Limits**
   - Set memory limits in Docker
   - Monitor CPU usage

3. **Scaling**
   - Consider load balancer for multiple instances
   - Use managed services for auto-scaling

### Monitoring

1. **Logging**
   - Configure application logging
   - Use cloud provider logging (CloudWatch, Stackdriver)

2. **Health Checks**
   - Implement health check endpoint
   - Monitor uptime

3. **Error Tracking**
   - Use Sentry or similar service
   - Set up alerts

---

## 🔧 Configuration Files

### Streamlit Config (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Environment Variables

```bash
# .env (for local development)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

---

## 📊 Resource Requirements

### Minimum Requirements

- **CPU**: 1 vCPU
- **RAM**: 1 GB
- **Storage**: 1 GB
- **Bandwidth**: 1 GB/month (for small teams)

### Recommended for Production

- **CPU**: 2 vCPUs
- **RAM**: 4 GB
- **Storage**: 10 GB
- **Bandwidth**: 10 GB/month

### Expected Load

- **Concurrent Users**: 10-50 (typical)
- **Response Time**: < 2 seconds (optimization)
- **Uptime Target**: 99.9%

---

## 🧪 Testing Before Deployment

```bash
# Run local tests
streamlit run streamlit_app.py

# Test on different devices
# - Desktop browser (Chrome, Firefox, Safari)
# - Mobile browser
# - Tablet

# Load testing (optional)
# Use Apache Bench or Locust for load testing
ab -n 100 -c 10 http://localhost:8501/
```

---

## 📝 Deployment Checklist

- [ ] Test application locally
- [ ] Update README with deployment instructions
- [ ] Configure environment variables
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall/security groups
- [ ] Set up monitoring and logging
- [ ] Configure backups (if needed)
- [ ] Test in production environment
- [ ] Document deployment process
- [ ] Train operators on access
- [ ] Set up support contact

---

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -ti:8501

# Kill process
kill -9 <PID>
```

**Module not found:**
```bash
# Verify virtual environment
which python
pip list

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**Memory issues:**
- Increase container/instance memory
- Optimize data processing
- Use pagination for large datasets

**Connection refused:**
- Check firewall rules
- Verify port configuration
- Check application logs

---

## 📞 Support

For deployment assistance:
- Email: devops@greenstrand.com
- Documentation: This guide
- GitHub Issues: (if applicable)

---

**Last Updated:** 2025-10-24
