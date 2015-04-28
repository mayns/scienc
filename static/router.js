var Router = require('ampersand-router');
var ProjectsView = require('./views/projects');
var Projects = require('./models/projects');
var templates = require('./templates/templates');

var AppRouter = Router.extend({
    routes: {
        "": "projects",
        "scientists": "scientists",
        "scientist/:id": "scientist",
        "scientist/my-projects": "myProjects"
    },
    projects: function () {
        var self = this;
        var projects = new Projects();

        projects.on('sync', function(model, data, xhr){
            self.trigger('newPage', new ProjectsView({
                model: model,
                template: templates.project
            }));
        });

        projects.fetch();
    },
    scientists: function () {

    },
    scientist: function () {

    }

});

module.exports = AppRouter;
//<app-route path="/" element="project-list"></app-route>
//<app-route path="/scientists" element="scientists-list"></app-route>
//<app-route path="/scientist/my-projects" element="my-projects"></app-route>
//<app-route path="/scientist/:id" element="scientist-page"></app-route>
//<app-route path="/project/:id" element="project-page"></app-route>
//<app-route path="/project" element="project-modify"></app-route>
//<app-route path="/signup" element="scientist-modify"></app-route>
//<app-route path="/page-not-found" element="page-not-found"></app-route>
//<app-route path="/search" element="search-page"></app-route>
//<app-route path="*" redirect="/page-not-found"></app-route>