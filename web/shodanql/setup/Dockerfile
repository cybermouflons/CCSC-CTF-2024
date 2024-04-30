FROM node:20

WORKDIR /app

COPY package*.json ./

COPY routes/ routes/
COPY static/ static/
COPY views/ views/
COPY middleware/ middleware/
COPY server.js server.js
COPY database.js database.js


# COPY database.db database.db


RUN npm install


EXPOSE 3000
CMD ["npm", "run", "dev"] # Develpment only

# CMD ["npm", "run", "start"] # prod