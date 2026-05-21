# Build de l'application React
# On utilise node:20-alpine pour minimiser la taille de l'image intermediaire.
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --silent
COPY . .

# VITE_API_URL est l'URL de l'API vue depuis le navigateur de l'utilisateur.
# En production Docker, le navigateur appelle localhost:8000 (port expose par le service api).
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# Serveur Nginx pour les fichiers statiques
# L'image builder n'est pas conservee dans l'image finale - seul /dist est copie.
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
