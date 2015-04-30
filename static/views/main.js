var app = require('ampersand-app');
var View = require('ampersand-view');

var MainView = View.extend({
	events: {
		'click .js-link': 'handleLinkClick'
	},
	handleLinkClick: function (e) {
        var link = e.target;
        var path = link.pathname.slice(1);
		e.preventDefault();
		app.router.navigate(path);
	}
});

module.exports = MainView;