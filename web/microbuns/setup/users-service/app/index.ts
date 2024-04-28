import express from "express";
import { randomBytes } from "crypto";
import { Database } from "bun:sqlite";

const PORT = Bun.env.BUN_SERVER_PORT ?? 8081;

const app = express();
app.use(express.json());

const db = new Database();

db.query(
  `CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);`
).run();

db.prepare(
  `INSERT INTO users (username, password)
  SELECT 'admin', '${await Bun.password.hash(randomBytes(32))}'
  WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');`
).run();

app.post("/register", async (req, res) => {
  const { username, password } = req.body;

  const pHash = await Bun.password.hash(password);

  const exists = db
    .query(`SELECT * FROM users WHERE username = $username LIMIT 1`)
    .get({ $username: username });

  if (exists) {
    res.status(400).json({ error: "already exists" });
    return;
  }

  db.prepare(
    `INSERT INTO users (username, password)
    SELECT $username, $password
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = $username);`
  ).run({
    $username: username,
    $password: pHash,
  });

  res.status(200).json({ success: 200 });
});

app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  const user = db
    .query(`SELECT * FROM users WHERE username = $username LIMIT 1`)
    .get({
      $username: username,
    });

  if (!user) {
    res.json({ error: "does not exist" });
    return;
  }

  // @ts-ignore
  if (Bun.password.verifySync(password, user?.password)) {
    // @ts-ignore
    res.json({ ...user, password: "" });
    return;
  }

  res.json({ error: "denied" });
});

app.get("/:id", (req, res) => {
  const user = db.query(`SELECT * FROM users WHERE id = $id LIMIT 1`).get({
    $id: req.params.id,
  });
  // @ts-ignore
  res.json({ ...user, password: "" });
});

app
  .listen(PORT, () => {
    console.log(`users-service listening on port ${PORT}...`);
  })
  .setTimeout(10 * 1000);
