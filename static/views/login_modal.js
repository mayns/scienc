var BaseView = require('./base');
var AppInputView = require('./input');
var View = require('ampersand-view');
var FormView = require('ampersand-form-view');
var templates = require('../templates/templates');

var LoginModalView = View.extend({
	template: templates.login_modal,
	render: function() {
		var self = this;

		self.renderWithTemplate();
		self.form = new FormView({
			el: self.query('form'),
			model: app.user,
			autoAppend: false,
			fields:  [
				new AppInputView({
					el: self.query('.js-email'),
					name: 'email',
		            value: '',
					placeholder: 'E-mail',
		            required: true
				}),
				new AppInputView({
					el: self.query('.js-password'),
					name: 'pwd',
					placeholder: 'Password',
		            value: '',
		            required: true
				})
			],
			submitCallback: function(data) {
				this.model.signIn(data);
			}
		});
		self.registerSubview(self.form);
		return this;
	}
});

module.exports = LoginModalView;