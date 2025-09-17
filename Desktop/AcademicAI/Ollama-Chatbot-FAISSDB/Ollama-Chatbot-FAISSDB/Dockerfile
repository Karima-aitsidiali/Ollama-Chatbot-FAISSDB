<<<<<<< HEAD
FROM python:3.11-slim

WORKDIR /BackEnd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ajoute cette ligne pour télécharger le tokenizer
# RUN pip install --upgrade nltk
# RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
=======
# Build stage
FROM node:20 AS build
WORKDIR /FrontEnd
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Serveur statique
FROM nginx:alpine
COPY --from=build /FrontEnd/dist /usr/share/nginx/html
EXPOSE 80
>>>>>>> 54544bd55cc319a89096b7e03467826462311e83
