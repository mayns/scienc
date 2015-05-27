var FormView = require('ampersand-form-view');
var BaseView = require('ampersand-view');
var templates = require('../templates/templates');
var AppInputView = require('./input');

var HighEducationsView = BaseView.extend({
	template: templates.scientist_form.high_educations,
	bindings: {
		'model.city': {
			type: 'value',
			hook: 'city'
		},
		'model.chair': {
			type: 'value',
			hook: 'chair'
		},
		'model.country': {
			type: 'value',
			hook: 'country'
		},
		'model.degree': {
			type: 'value',
			hook: 'degree'
		},
		'model.faculty': {
			type: 'value',
			hook: 'faculty'
		},
		'model.graduation_year': {
			type: 'value',
			hook: 'graduation_year'
		},
		'model.university': {
			type: 'value',
			hook: 'university'
		}
	}
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
		'model.first_name': {
			type: 'value',
			hook: 'first_name'
		},
		'model.last_name': {
			type: 'value',
			hook: 'last_name'
		},
		'model.middle_name': {
			type: 'value',
			hook: 'middle_name'
		},
		'model.gender': [
			{
				type: 'switchAttribute',
			    hook: 'gender-m',
				name: 'checked',
			    cases: {
			        m: {
				        checked: 'checked'
			        }
			    }
			},
			{
				type: 'switchAttribute',
			    hook: 'gender-f',
				name: 'checked',
			    cases: {
			        f: {
				        checked: 'checked'
			        }
			    }
			}
		],
		'model.dob': {
			type: 'value',
			hook: 'dob'
		},
		'model.location.country': {
			type: 'value',
			hook: 'location.country'
		},
		'model.location.city': {
			type: 'value',
			hook: 'location.city'
		},
		'model.middle_education.country': {
			type: 'value',
			hook: 'middle_education.country'
		},
		'model.middle_education.city': {
			type: 'value',
			hook: 'middle_education.city'
		},
		'model.middle_education.school': {
			type: 'value',
			hook: 'middle_education.school'
		},
		'model.middle_education.graduation_year': {
			type: 'value',
			hook: 'middle_education.graduation_year'
		},
		'model.interests': {
			type: 'value',
			hook: 'interests'
		},
		'model.about': {
			type: 'value',
			hook: 'about'
		}
	},
	template: templates.scientist_form.main,
	render: function () {
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

		self.high_educations = self.renderCollection(self.model.high_education, HighEducationsView, self.query('.js-high-educations'));
		self.publications = self.renderCollection(self.model.publications, PublicationsView, self.query('.js-publications'));
		self.contacts = self.renderCollection(self.model.contacts, ContactsView, self.query('.js-contacts'));
		return this;
	},
	addItem: function (e) {
		var data = e.target.dataset;
		var type = data.type;

		this.model[type].add({});
	},
	deleteItem: function (e) {
		var data = e.target.dataset;
		var id = data.cid;
		var type = data.type;

		this.model[type].remove(id);
	}
});


module.exports = ScientistFormView;