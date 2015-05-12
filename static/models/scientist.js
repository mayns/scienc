var BaseModel = require('./base');

var ScientistModel = BaseModel.extend({
	urlRoot: '/api/scientist',
	idAttribute: 'id',
	props: {
		id: ['string', true, ''],
		first_name: ['string', true, ''],
		middle_name: ['string', true, ''],
		last_name: ['string', true, ''],
		image_url: ['string', true,  '/static/images/profile.svg'],
		dob: 'string',
		gender: {
			type: 'string',
			values: ['f', 'm']
		},
		location: 'object',
		middle_education: 'array',
		high_education: 'array',
		publications: 'array',
		interests: 'array',
		about: 'string',
		contacts: 'array'
	}
});

module.exports = ScientistModel;