const express = require('express');
const nunjucks = require('nunjucks');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const http = require('http');
const Database = require('./database.js')
const fs = require('fs');

const jose = require("node-jose");

app = express();

var httpServer = http.createServer(app);
const routes = require('./routes'); 
const db = new Database('database.db');


app.use(bodyParser.urlencoded());
app.use(express.json());
app.use(cookieParser());

nunjucks.configure('views', {
  autoescape: true,
  express: app
});

app.set('view engine', 'nunjucks');

app.set('views', './views');
app.use(express.static('static'));


app.use(routes(db));


const keyStore = jose.JWK.createKeyStore();

keyStore.generate("RSA", 2048, { alg: "RS256", use: "sig" }).then((result) => {
  fs.writeFileSync(
    "jwks.json",
    JSON.stringify(keyStore.toJSON(true), null, "  ")
  );
});


(async() => {

  await db.connect();
  await db.migrate();


  httpServer.listen(3000, () => {
      console.log(`Server running at http://${process.env.host}/`);
  });

})();