# HealthCore — AWS Deployment Guide

## AWS Services Required
- **EC2** — t2.micro (server to run Django and Nginx)
- **RDS** — PostgreSQL 16 (managed database)
- **ElastiCache** — Redis (managed Redis for Celery)
- **S3** — Static and media file storage
- **Route 53** — Domain name (optional)

## Architecture
Internet → EC2 (Nginx + Gunicorn) → RDS (PostgreSQL)
→ ElastiCache (Redis)
→ S3 (Static/Media)

## Estimated Monthly Cost
- EC2 t2.micro — $8.50/month (or free tier if eligible)
- RDS db.t3.micro — $15/month (or free tier if eligible)
- ElastiCache cache.t3.micro — $12/month
- S3 — ~$1/month
- **Total — ~$36/month**

## Step by Step Deployment

### 1. Launch EC2 Instance
1. Go to AWS Console → EC2 → Launch Instance
2. Choose Ubuntu 24.04 LTS
3. Instance type: t2.micro
4. Create or select a key pair (save the .pem file safely)
5. Security group rules:
   - SSH: port 22 from your IP
   - HTTP: port 80 from anywhere
   - HTTPS: port 443 from anywhere
   - Custom: port 8000 from anywhere (for testing)

### 2. Launch RDS PostgreSQL
1. Go to AWS Console → RDS → Create Database
2. Engine: PostgreSQL 16
3. Template: Free tier
4. DB name: healthcore_db
5. Username: healthcore_user
6. Password: (save this securely)
7. Make sure it's in the same VPC as your EC2

### 3. Launch ElastiCache Redis
1. Go to AWS Console → ElastiCache → Create
2. Engine: Redis
3. Node type: cache.t3.micro
4. Make sure it's in the same VPC as your EC2

### 4. Create S3 Bucket
1. Go to AWS Console → S3 → Create Bucket
2. Name: healthcore-media-files
3. Region: same as EC2
4. Uncheck "Block all public access" for media files

### 5. Connect to EC2
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 6. Install Dependencies on EC2
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3-pip python3-venv nginx postgresql-client git

# Install Node for frontend build
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### 7. Clone the Repository
```bash
cd /home/ubuntu
git clone https://github.com/parwatpandit/healthcore-backend.git
git clone https://github.com/parwatpandit/healthcore-frontend.git
```

### 8. Set Up Backend
```bash
cd healthcore-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn boto3 django-storages
```

### 9. Set Environment Variables
```bash
cp deployment/.env.production .env
nano .env  # fill in your actual values
```

### 10. Run Migrations and Collect Static
```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 11. Build Frontend
```bash
cd /home/ubuntu/healthcore-frontend
npm install
npm run build
sudo cp -r dist/* /var/www/healthcore/
```

### 12. Start Services
```bash
sudo systemctl enable healthcore
sudo systemctl start healthcore
sudo systemctl enable nginx
sudo systemctl start nginx
```