const express = require('express');
const { verifyToken, createToken }  = require('../middleware/authMiddleware');
const fs = require('fs');
const router = express.Router({ caseSensitive: true });
const jose = require("node-jose");


const response = data => ({ message: data });


router.get('/',verifyToken, async (req, res) => {

    const items = await db.items();

    return res.render('index.html', { items: items });
});


router.get('/item/:item', verifyToken, async (req, res) => {

    const item = await db.item(req.params.item);
    const verified_token = req.verified_token

    if(verified_token.skill_points > item.skill_points){
        return res.render('item.html', { item: item});
    }

    return res.status(401).json({ error: 'A player with your skill set cannot acquire this item! Level up first' });

});


router.get('/login', (req, res) => {
    return res.render('login.html');
});


router.post('/login', async (req, res) => {
    const { username, password } = req.body;
  
    if (username && password) {

        return db.login(username, password)
            .then(async user => {
                token = await createToken(user)
                res.cookie("session", token).redirect('/');
            })
            .catch(() => res.status(403).send(response('Invalid username or password!')));
    }
    return res.status(500).send(response('Missing parameters!'));
});


router.get('/register', (req, res) => {
    return res.render('register.html');
});

router.post('/register', async (req, res) => {
    const { username, password } = req.body;

    user_exists = await db.user_exists(username);
    if(user_exists){
        return res.status(500).send(response('Username already exists'));
    }

    await db.register(username, password, 1000);
  
    // Redirect to login page
    return res.redirect('/login');
  });


router.get('/logout', (req, res) => {

    return res.clearCookie('session').redirect('/login');
});

// Define route handler for .well-known/jwks.json
app.get('/jwks.json', async (req, res) => {
    try {
        // Read the JWKS file
        const jwks = fs.readFileSync('jwks.json', 'utf8');

        const keyStore = await jose.JWK.asKeyStore(jwks.toString());
        res.send(keyStore.toJSON());

    } catch (error) {

        console.error('Failed to read JWKS file:', error);
        return res.status(500).send(response('Failed to read JWKS file'));
    }
});

module.exports = database => {
    db = database;
    return router;
};

