#!/bin/bash

# === CONFIGURATION ===
PROJECT_ID="inehealth-mvp-462020"   # ✅ Replace if needed
REGION="us-central1"
SERVICE_NAME="ussd-gateway"
DB_INSTANCE_NAME="health-db"
DB_NAME="ninehealth"
DB_USER="postgres"
DB_PASS="9inehealth_secure"
CONTAINER_IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Setting project..."
gcloud config set project $PROJECT_ID

echo "Creating Cloud SQL instance..."
gcloud sql instances create $DB_INSTANCE_NAME \
  --database-version=POSTGRES_14 \
  --cpu=1 \
  --memory=4GB \
  --region=$REGION \
  --root-password=$DB_PASS

echo "Creating database..."
gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE_NAME

echo "Building Docker image..."
gcloud builds submit --tag $CONTAINER_IMAGE ussd_gateway/

echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image=$CONTAINER_IMAGE \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars="DB_INSTANCE=$DB_INSTANCE_NAME,DB_NAME=$DB_NAME,DB_USER=$DB_USER,DB_PASS=$DB_PASS" \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:$DB_INSTANCE_NAME
