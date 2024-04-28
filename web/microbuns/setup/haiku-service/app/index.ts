import express from "express";
import { Database } from "bun:sqlite";

const PORT = Bun.env.BUN_SERVER_PORT ?? 8082;

const app = express();
app.use(express.json());

const db = new Database();

const FLAG = Bun.env.FLAG ?? "CCSC{dummy_flag}";

db.prepare(
  `CREATE TABLE IF NOT EXISTS haikus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    haiku TEXT,
    is_private BOOLEAN);`
).run();

const defaultPrivateHaiku = `Echoes whisper loud,
${FLAG},
Legends rise unbowed.`;

db.prepare(
  `INSERT INTO haikus (author_id, haiku, is_private)
  SELECT 1, '${defaultPrivateHaiku}', true
  WHERE NOT EXISTS (SELECT 1 FROM haikus WHERE author_id = 1 AND haiku = '${defaultPrivateHaiku}');`
).run();

const defaultPublicHaiku = `Digital shadows,
Cyber warriors take their stand,
Legends born in code.`;

db.prepare(
  `INSERT INTO haikus (author_id, haiku, is_private)
  SELECT 1, '${defaultPublicHaiku}', false
  WHERE NOT EXISTS (SELECT 1 FROM haikus WHERE author_id = 1 AND haiku = '${defaultPublicHaiku}');`
).run();

const defaultPublicHaiku2 = `Beneath neon skies,
Cybernetic echoes rise,
Legends in disguise.`;

db.prepare(
  `INSERT INTO haikus (author_id, haiku, is_private)
  SELECT 1, '${defaultPublicHaiku2}', false
  WHERE NOT EXISTS (SELECT 1 FROM haikus WHERE author_id = 1 AND haiku = '${defaultPublicHaiku2}');`
).run();

app.post("/create", (req, res) => {
  const { author_id, haiku, is_private = false } = req.body;

  if (
    typeof author_id !== "number" ||
    typeof haiku !== "string" ||
    typeof is_private !== "boolean"
  ) {
    res.json({ error: 400 });
    return;
  }

  db.prepare(
    `INSERT INTO haikus (author_id, haiku, is_private)
    SELECT $author_id, $haiku, $is_private
    WHERE NOT EXISTS (SELECT 1 FROM haikus WHERE author_id = $author_id AND haiku = $haiku);`
  ).run({
    $author_id: author_id,
    $haiku: haiku,
    $is_private: is_private,
  });

  res.json({ success: 200 });
});

app.get("/public", (req, res) => {
  const results = db
    .query(`SELECT * FROM haikus WHERE is_private = false`)
    .all();
  res.json({ results });
});

app.get("/public/:author_id", (req, res) => {
  const results = db
    .query(
      `SELECT * FROM haikus WHERE author_id = $author_id AND is_private = false`
    )
    .all({
      $author_id: req.params.author_id,
    });
  res.json({ results });
});

app.get("/private/:author_id", (req, res) => {
  const results = db
    .query(
      `SELECT * FROM haikus WHERE author_id = $author_id AND is_private = true`
    )
    .all({
      $author_id: req.params.author_id,
    });
  res.json({ results });
});

app.get("/all/:author_id", (req, res) => {
  const results = db
    .query(`SELECT * FROM haikus WHERE author_id = $author_id`)
    .all({
      $author_id: req.params.author_id,
    });
  res.json({ results });
});

app
  .listen(PORT, () => {
    console.log(`haiku-service listening on port ${PORT}...`);
  })
  .setTimeout(10 * 1000);
