
const jwksClient = require('jwks-rsa');
const fs = require('fs');
const jwt = require('jsonwebtoken');
const jose = require("node-jose");
const dns = require('dns')
var url = require("url");


async function verifyToken(req, res, next) {

    const token = req.cookies.session;

    if (!token) return res.redirect('/login');

    try {

        const decoded = jwt.decode(token, { complete: true }); 
        const client = jwksClient({
            jwksUri: decoded.header.jku 
        });

        const jku_url = url.parse(client.options.jwksUri).hostname

        ip_address = await new Promise((resolve, reject) => dns.lookup(jku_url, {family: 4}, (err, result) => {
                if (err) {
                    reject(err);
                  } else {
                    resolve(result)
                  }
        }))
       
        if(ip_address !== "127.0.0.1"){
            return res.status(401).json({ error: 'Sneaky sneaky...' });
        }

        const key  = await client.getSigningKey()
        publicKey = key.getPublicKey()
        req.verified_token = jwt.verify(token, publicKey);
        
        return next();
    } catch (error) {
        console.error( error);
        return res.status(401).json({ error: 'Invalid token' });
    }


};

async function createToken(user){

    try{

        payload = JSON.stringify({
            id: user.id,
            role: user.role
        })
    

        const jkuUrl = 'http://localhost:3000/jwks.json';
        const JWKeys = fs.readFileSync("jwks.json");
        const keyStore = await jose.JWK.asKeyStore(JWKeys.toString());
        const [key] = keyStore.all({ use: "sig" });
        const opt = { compact: true, jwk: key, fields: { typ: "jwt", jku: jkuUrl } };
        const token = await jose.JWS.createSign(opt, key).update(payload).final();

        return token
    }
    catch(error){
        console.error('Error creating token:', error);
        throw error; // Rethrow the error for further handling

    }
   
}

function isAdmin(req, res, next){

    if(req.verified_token.role !== "admin"){
        return res.status(401).json({ error: 'Only admin users allowed! Go away >_<' });
    }

    return next();
}


module.exports = {
    verifyToken,
    createToken,
    isAdmin
};

