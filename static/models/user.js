var BaseModel = require('./base');
var sync = require('ampersand-sync');
require('setimmediate');

var User = BaseModel.extend({
	initialize: function() {
		var self = this;

		self.on('change:id', function() {
			self.isLoggedIn = Boolean(self.id);
		});
	},
	urlRoot: '/api/user',
	props: {
		id: ['string', false, ''],
		image_url: ['string', false, '/static/images/profile.svg'],
		desired_vacancies: 'array',
		liked_projects: 'array',
		managing_project_ids: 'array'
	},
	session: {
		isLoggedIn: 'boolean',
		xsrf: 'string'
	},
	initialize: function() {
		var self = this;
		var user = this.getCookie('scientist');
		var xsrf = this.getCookie('_xsrf');

		if (user) {
			self.set('xsrf', xsrf);
			setImmediate(function(){
				self.fetch();
			});
		}
		else if (!xsrf) {
			setImmediate(function(){
				self.fetch();
			});
		}
		else {
			self.set('xsrf', xsrf);
			setImmediate(function(){
				self.trigger('sync');
			});
		}
	},
	signIn: function (data) {
		var self = this;
		var formData = new FormData();

		formData.append('data', JSON.stringify(data));
		sync('create', this, {
			url: '/api/login',
			data: formData,
			success: function() {
				self.fetch();
			},
			error: function() {
				console.error(arguments);
			}
		});
	},
	signOut: function () {
		var self = this;

		sync('create', this, {
			url: '/api/logout',
			data: new FormData(),
			success: function() {
				self.isLoggedIn = false;
			},
			error: function() {
				console.error(arguments);
			}
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