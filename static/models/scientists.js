var Model = require('ampersand-model');

var Scientists = Model.extend({
    urlRoot: '/api/scientists',
	props: {
		scientists: 'array'
	}
});

module.exports = Scientists;