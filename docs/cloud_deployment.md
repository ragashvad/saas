# Cloud & Production Deployment Guide

1) Dockerize services
- Build backend: docker build -t saas-backend backend/
- Build dashboard: docker build -t saas-dashboard dashboard/

2) Run locally with Docker
- docker run -p 5000:5000 saas-backend
- docker run -p 8501:8501 saas-dashboard

3) Deploy options
- Render.com: create two web services, point each to repo subfolder; set build & start commands or use Docker.
- AWS Elastic Beanstalk: create two apps (backend + dashboard) or put behind load balancer. Use gunicorn for Flask in production.

4) Secrets & env
- Use environment variables for secrets.
- Use cloud storage (S3) for uploaded files in production.

5) Production tips
- Replace in-memory user store with a DB (Postgres).
- Use HTTPS and authentication (OAuth2/JWT).
- Use managed ML endpoints for scalability.