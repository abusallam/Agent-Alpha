FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm cache clean --force && npm install

COPY . .
RUN npm run build
RUN pwd
RUN ls -la /app
RUN ls -la /app/dist

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
