'use strict';

var app = require('ampersand-app');
var MainView = require('./views/main');
var AppBarView = require('./views/app_bar');
var User = require('./models/user');
var Router = require('./router');
var dom = require('ampersand-dom');
var templates = require('./templates/templates');

dom.byId = function(id) {
    return document.getElementById(id);
};

app.extend({
	init: function () {
        var self = this,
            views = {},
            router = new Router(),
            user = new User();

        app.views = views;
        app.router = router;
        app.user = user;

        user.fetch();

		views.main = new MainView({
			el: dom.byId('content')
		});
        views.appBar = new AppBarView({
            el: dom.byId('appBar'),
            model: user
        });

        window.app = app;
		// Create and fire up the router
		router.history.start();
	}
});

app.init();