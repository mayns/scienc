var Model = require('ampersand-model');
var sync = require('ampersand-sync');
require('setimmediate');

var User = Model.extend({
	urlRoot: '/api/user',
	props: {
		id: 'number',
		image_url: ['string', false, '/static/images/profile.svg'],
		desired_vacancies: 'array',
		liked_projects: 'array',
		managing_project_ids: 'array'
	},
	session: {
		isLoggedIn: 'boolean',
		xsrf: 'string'
	},
	initialize: function () {
		var self = this;
		var user = this.getCookie('scientist');
		var xsrf = this.getCookie('_xsrf');

		if (user || !xsrf) {
			this.fetch();
		}
		else {
			this.set('xsrf', xsrf);
			setImmediate(function(){
				self.trigger('sync');
			});
		}
	},
	signIn: function (data) {
		var formData = new FormData();
		formData.append('data', JSON.stringify(data));

		sync('create', this, {
			url: '/api/login',
			data: formData
		});
	},
	signOut: function () {
		sync('create', this, {
			url: '/api/logout'
		});
	},
	getCookie: function (name) {
		var match = document.cookie.match("\\b" + name + "=([^;]*)\\b");
		return match ? match[1] : match;
	}
});

module.exports = User;

//desired_vacancies: []
//id: 2
//image_url: "https://en.gravatar.com/userimage/39116033/0b1c1ef31de9d584943a47db3a03143a.jpg?size=60"
//liked_projects: []
//managing_project_ids: [1]