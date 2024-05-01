
function isAdmin(req, res, next){


    if(req.session.user && req.session.user.is_admin){
            
        next()

    }else{
        return res.render('login.html', { error: 'Log in as admin!'} )

    }

    

}


module.exports = {
    isAdmin
};

