var View = require('ampersand-view');
var templates = require('../templates/templates');

var ProjectsView = View.extend({
    template: templates.projects
});

module.exports = ProjectsView;