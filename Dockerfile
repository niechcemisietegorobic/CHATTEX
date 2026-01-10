# FROM node:25 AS frontend-stage

# WORKDIR /frontend

# COPY frontend/package*.json /frontend/
# RUN npm install

# COPY frontend/ /frontend/
# RUN npm run build

FROM python:3.13

WORKDIR /backend

COPY backend/requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /backend/
# COPY --from=frontend-stage /frontend/dist/ /backend/static/

EXPOSE 8000

CMD ["python3", "-m", "gunicorn", "-w", "4", "'app:app'"]

