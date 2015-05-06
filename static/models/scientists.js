var Model = require('ampersand-model');

var Scientists = Model.extend({
    urlRoot: '/api/scientists',
	props: {
		data: 'array'
	}
});

module.exports = Scientists;