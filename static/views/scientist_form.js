var FormView = require('ampersand-form-view');
var BaseView = require('ampersand-view');
var templates = require('../templates/templates');
var AppInputView = require('./input');

var HighEducationsView = BaseView.extend({
	template: templates.scientist_form.high_educations
});


var PublicationsView = BaseView.extend({
	template: templates.scientist_form.publications
});

var ContactsView = BaseView.extend({
	template: templates.scientist_form.contacts
});

var ScientistFormView = BaseView.extend({
	events: {
		'click .js-add-item': 'addItem',
		'click .js-delete-item': 'deleteItem'
	},
	bindings: {

	},
    template: templates.scientist_form.main,
	render: function() {
		var self = this;

		self.renderWithTemplate();
		//self.form = new FormView({
		//	el: self.query('.js-form'),
		//	model: self.model,
		//	autoAppend: false,
		//	fields:  [
		//		new AppInputView({
		//			el: self.query('.js-first-name'),
		//			name: 'first_name',
		//            value: self.model.first_name,
		//			placeholder: 'Иван',
		//            required: true
		//		}),
		//		new AppInputView({
		//			el: self.query('.js-last-name'),
		//			name: 'last_name',
		//			placeholder: 'Иванов',
		//            value: self.model.last_name,
		//            required: true
		//		}),
		//		new AppInputView({
		//			el: self.query('.js-middle-name'),
		//			name: 'middle_name',
		//			placeholder: 'Иванович',
		//            value: self.model.middle_name,
		//            required: true
		//		})
		//	],
		//	validCallback: function (valid) {
         //       if (valid) {
         //           console.log('The form is valid!');
         //       } else {
         //           console.log('The form is not valid!');
         //       }
         //   },
		//	submitCallback: function(data) {
		//		console.log(data);
		//	}
		//});
		//self.registerSubview(self.form);

		self.high_educations = self.renderCollection(self.model.high_educations, HighEducationsView, self.query('.js-high-educations'));
		self.publications = self.renderCollection(self.model.publications, PublicationsView, self.query('.js-publications'));
		self.contacts = self.renderCollection(self.model.contacts, ContactsView, self.query('.js-contacts'));
		return this;
	},
	addItem: function(e) {
		var data = e.target.dataset;
		var type = data.type;

		this.model[type].add({});
	},
	deleteItem: function(e) {
		var data = e.target.dataset;
		var id = data._id;
		var type = data.type;

		this.model[type].remove(id);
	}
});


module.exports = ScientistFormView;