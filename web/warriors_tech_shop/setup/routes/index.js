const express = require('express');
const { verifyToken, createToken, isAdmin }  = require('../middleware/authMiddleware');
const fs = require('fs');
const router = express.Router({ caseSensitive: true });
const jose = require("node-jose");


const response = data => ({ message: data });


router.get('/',verifyToken, async (req, res) => {

    const items = await db.items();
    const user = await db.get_user(req.verified_token.id);

    const is_admin = req.verified_token.role === "admin" ? true : false;

    return res.render('index.html', { items: items, user: user , is_admin: is_admin});
});

// Purchase item
router.get('/item/:item', verifyToken, async (req, res) => {

    const item = await db.item(req.params.item);
    const user = await db.get_user(req.verified_token.id);

    if(user.bank < item.price){
        return res.status(401).json({ error: 'Not enough sorry, apparently admin users have the ability to add money.'});
    }

    balance = user.bank - item.price
    balance = Math.round(balance * 100) / 100
    
    await db.update_balance(user.id, balance)

    return res.render('item.html', {item: item})
});


router.get('/login', (req, res) => {
    return res.render('login.html');
});

router.get('/admin',verifyToken, isAdmin, (req, res) => {
    return res.render('admin.html');
});

router.post('/admin', verifyToken, isAdmin, async (req, res) => {
    
    const user = await db.get_user(req.verified_token.id);

    let balance = user.bank + req.body.bank
    balance = Math.round(balance * 100) / 100

    await db.update_balance(user.id, balance)

    return res.redirect('/');
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

    await db.register(username, password, 'user', 1000);
  
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

