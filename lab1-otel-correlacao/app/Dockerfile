FROM node:18-slim
WORKDIR /app
COPY package.json /app/
RUN npm install --omit=dev
COPY . /app/
EXPOSE 8080
CMD ["node", "start.js"]
