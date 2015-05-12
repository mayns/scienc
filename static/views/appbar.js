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

		self.model.once('sync', self.onFirstSync, self);
	},
	template: templates.appbar,
	onFirstSync: function() {
		var self = this;

		self.render();

		self.model.on('change:isLoggedIn', function(model, value){
			if (value) {
				self.closeSignInModal();
			}
			else {
				self.model.clear();
			}
			self.render();
		});
	},
	openSignInModal: function () {
		var self = this;
		var loginView = new LoginModalView().render();
		var modal = new ModalView({
			view: templates.modal,
			contentView: loginView
		});

		modal.openIn('body');
		self.modal = modal;
	},
	closeSignInModal: function() {
		this.modal && this.modal.close();
	},
	signOut: function() {
		this.model.signOut();
	}
});

module.exports = AppBarView;