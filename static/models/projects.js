var BaseModel = require('./base');

var Projects = BaseModel.extend({
    urlRoot: '/api/projects',
	props: {
		data: 'array'
	}
});

module.exports = Projects;