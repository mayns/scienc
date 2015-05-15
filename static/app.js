'use strict';

var app = require('ampersand-app');
var ContentView = require('./views/content');
var AppBarView = require('./views/appbar');
var MainView = require('./views/main');
var User = require('./models/user');
var Router = require('./router');
var dom = require('ampersand-dom');
var templates = require('./templates/templates');
var counter = 0;

dom.byId = function(id) {
    return document.getElementById(id);
};

app.extend({
	init: function () {
        var self = this,
            views = {},
            models = {},
            router = new Router(),
            user = new User();

        app.views = views;
        app.models = models;
        app.router = router;
        app.user = user;

        views.main = new MainView({
	        el: document.body
        });

		views.content = new ContentView({
			el: dom.byId('content')
		});
        views.appBar = new AppBarView({
            el: dom.byId('appBar'),
            model: user
        });
		// Wait for user to get xsrf token
		user.once('sync', function(){
			// Create and fire up the router
			router.history.start();
		});

		// Global ref for debugging
        window.app = app;
	},
	getId: function() {
		return counter++;
	}
});

app.init();