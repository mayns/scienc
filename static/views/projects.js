var BaseView = require('./base');
var templates = require('../templates/templates');

var ProjectsView = BaseView.extend({
    template: templates.projects
});

module.exports = ProjectsView;