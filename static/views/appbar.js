var BaseView = require('./base');
var ModalView = require('./modal');
var LoginModalView = require('./login_modal');
var templates = require('../templates/templates');

var AppBarView = BaseView.extend({
	events: {
		'click #signIn': 'openSignInModal',
		'click #signOut': 'signOut'
	},
	initialize: function () {
		var self = this;

		self.model.once('sync', function () {
			self.render();
		});
		self.model.on('change:isLoggedIn', function(){
			self.render();
		});
	},
	template: templates.appbar,
	openSignInModal: function () {
		var loginView = new LoginModalView().render();
		var modal = new ModalView({
			view: templates.modal,
			contentView: loginView
		});

		modal.openIn('body');
	},
	signOut: function() {
		this.model.signOut();
	}
});

module.exports = AppBarView;