FROM node:20

WORKDIR /app

COPY package*.json ./

COPY routes/ routes/
COPY middleware/ middleware/
COPY static/ static/
COPY views/ views/
COPY server.js server.js
COPY database.js database.js 

RUN npm install


EXPOSE 3000

CMD ["npm", "run", "start"]
# CMD ["npm", "run", "dev"]