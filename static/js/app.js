'use strict';

var app = require('ampersand-app');
//var MainView = require('./views/main');
var User = require('../models/user');
var Router = require('./router');


app.extend({
	init: function () {
		var user = new User();
        user.fetch();
		// Our main view
		//this.view = new MainView({
		//	el: document.body,
		//	model: this.me
		//});
		// Create and fire up the router
		this.router = new Router();
		this.router.history.start();
	}
});

app.init();