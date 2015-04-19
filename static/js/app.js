'use strict';

var app = require('ampersand-app');
//var MainView = require('./views/main');
//var User = require('./models/me');
var Router = require('./router');


app.extend({
	init: function () {
		//this.user = new User();
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