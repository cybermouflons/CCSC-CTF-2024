import express from "express";
import cookieParser from "cookie-parser";
import jwt from "jsonwebtoken";
import { randomBytes } from "crypto";

const app = express();
app.use(cookieParser());

const PORT = Bun.env.PORT ?? 8080;
const JWT_SECRET = randomBytes(32).toString("hex");

app.use(express.json());

app.set("view engine", "ejs");

// @ts-ignore
const authenticateJWT = (req, res, next) => {
  const token = req.cookies.token;

  if (!token) {
    return res.status(401).redirect("/login");
  }

  // @ts-ignore
  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    try {
      if (err) {
        return res.status(403).redirect("/login");
      }

      if (req?.query?.user_id) {
        if (parseInt(req.query.user_id) !== decoded.user.id) {
          return res.status(403).redirect("/login");
        }
      }

      if (req?.params?.user_id) {
        if (parseInt(req.params.user_id) !== decoded.user.id) {
          return res.status(403).redirect("/login");
        }
      }
    } catch (e) {
      return res.status(403).redirect("/login");
    }

    req.user = decoded.user;
    next();
  });
};

// Login endpoint
app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  const user = await fetch("http://users-service:8081/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  }).then((r) => r.json());

  if (user?.error) {
    return res.status(401).json({ message: "Invalid username or password" });
  }

  const token = jwt.sign(
    { user: { id: user.id, username: user.username } },
    JWT_SECRET
  );

  res.cookie("token", token, { httpOnly: true });

  res.status(200).json({ token });
});

// Register endpoint
app.post("/register", async (req, res) => {
  const { username, password } = req.body;

  const result = await fetch("http://users-service:8081/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  }).then((r) => r.json());

  if (result?.error) {
    res.status(400).json({ message: result?.error });
  }

  res.status(200).json({ message: "User registered successfully" });
});

app.get("/haikus", authenticateJWT, async (req, res) => {
  const result = await fetch(`http://haiku-service:8082/public`).then((r) =>
    r.json()
  );

  res.render("haikus", {
    haikus: result?.results ?? [],
    title: "All Public Haikus",
    // @ts-ignore
    user_id: req.user.id,
  });
});

app.get("/user/:user_id/profile", authenticateJWT, async (req, res) => {
  // @ts-ignore
  const userID = req.params.user_id;

  if (!userID) {
    res.status(400).json({ message: "user_id missing" });
    return;
  }

  const result = await fetch(`http://haiku-service:8082/all/${userID}`).then(
    (r) => r.json()
  );

  res.render("profile", {
    title: "Your Profile",
    // @ts-ignore
    user_id: req.user.id,
    // @ts-ignore
    username: req.user.username,
    haikus: result?.results ?? [],
    total_haikus: (result?.results ?? []).length,
  });
});

app.get("/user/:user_id/haikus/private", authenticateJWT, async (req, res) => {
  // @ts-ignore
  const userID = req.params.user_id;

  if (!userID) {
    res.status(400).json({ message: "user_id missing" });
    return;
  }

  const result = await fetch(
    `http://haiku-service:8082/private/${userID}`
  ).then((r) => r.json());

  res.render("haikus", {
    title: "My Private Haikus",
    haikus: result?.results ?? [],
    // @ts-ignore
    user_id: req.user.id,
  });
});

app.post("/haiku", authenticateJWT, (req, res) => {
  const { haiku, is_private = false } = req.body;

  fetch("http://haiku-service:8082/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // @ts-ignore
    body: JSON.stringify({ haiku, author_id: req.user.id, is_private }),
  });

  res.status(201).json({ message: "success" });
});

app.get("/register", (req, res) => {
  res.render("register");
});

app.get("/login", (req, res) => {
  res.render("login");
});

app.get("/*", (req, res) => {
  res.redirect("/login");
});

app
  .listen(PORT, () => {
    console.log(`backend-service listening on port ${PORT}...`);
  })
  .setTimeout(10 * 1000);
