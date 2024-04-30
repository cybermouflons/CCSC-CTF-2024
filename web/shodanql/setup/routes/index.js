const express = require('express')
const router = express.Router({ caseSensitive: true });
const { isAdmin }  = require('../middleware/authMiddleware');

const response = data => ({ message: data });

router.get('/', async (req, res) => {

    let systems
    let search
    const user = req.session.user

    console.log(user)

    try {
        if(req.query.ip){
            search = req.query.ip
            systems = await db.search(search)
        }
        else{
            systems = await db.getSystems();
        }

        return res.render('index.html', {user: user, systems: systems, search: search});
    }
    catch (error) {

        return res.render('index.html', {user: user, systems: null, error: error.message, search: search });
    }

});

router.get('/admin',isAdmin, (req, res) => {

    const flag = process.env.flag

    return res.render('admin.html', {flag: flag});
});


router.get('/login', (req, res) => {
    return res.render('login.html');
});

router.post('/login', async (req, res) => {
    
    const { username, password } = req.body;
  
    if (username && password) {

        return db.login(username, password)
            .then(async user => {
                if(user){
                    req.session.user = user
                    return res.redirect('/');
                }
                else{
                    return res.render('login.html', { error: 'Invalid username or password!'} )   
                }
            });
    }
    return res.status(500).send(response('Missing parameters!'));
});


router.get('/logout', (req, res) => {
    req.session = null
    return res.clearCookie('session').redirect('/login');
});


module.exports = database => {
    db = database;
    return router;
};

