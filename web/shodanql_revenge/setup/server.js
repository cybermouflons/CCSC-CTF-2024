const express = require('express');
const nunjucks = require('nunjucks');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const http = require('http');
const Database = require('./database.js')
const session = require('express-session')


app = express();

var httpServer = http.createServer(app);

const routes = require('./routes'); 

const db = new Database('database.db');


app.use(bodyParser.urlencoded());
app.use(express.json());
app.use(cookieParser());

app.use(session({
  name: 'session',
  secret: "secret_session_key-94r7uh"
}))

nunjucks.configure('views', {
  autoescape: true,
  express: app
});

app.set('view engine', 'nunjucks');

app.set('views', './views');
app.use(express.static('./static'));


app.use(routes(db));

app.use(function(err, req, res, next) {
    console.log(err)
    res.status(500).json({ message: 'You broke me :(' });
  });

(async() => {

await db.connect();
await db.migrate();


httpServer.listen(3003, () => {
    console.log(`Server running at http://localhost:3003/`);
});

})();