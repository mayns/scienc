/**
 * Created by mayns on 25/07/14.
 */

ScienceMates.Router.map(function(){
    this.resource('scientists');
    this.resource('scientist', {path: '/scientist/:id'});
    this.resource('scientistRegistration', {path: '/scientist/registration'});

    this.resource('projects');
    this.resource('project', {path: '/project/:id'});
    this.resource('addProject', {path: '/project/add'});
    this.resource('scientistProjects', {path: '/projects/:scientistID'});
});


ScienceMates.ApplicationRoute = Ember.Route.extend({
    actions: {
        openModal: function(modalName, model) {
            console.log(model);
            this.controller.set('model', model);
            return this.render(modalName, {
                into: 'application',
                outlet: 'modal'
            });
        },
        closeModal: function() {
           return this.disconnectOutlet({
               outlet: 'modal',
               parentView: 'application'
           });
        }
    }
});

 ////////////////
// Login modal //
////////////////

ScienceMates.ModalController = Ember.ObjectController.extend({
  actions: {
    close: function() {
      return this.send('closeModal');
    }
  }
});

ScienceMates.ModalDialogComponent = Ember.Component.extend({
  actions: {
    close: function() {
      return this.sendAction();
    }
  }
});


 ///////////////
// Scientist //
//////////////

// /scientists
ScienceMates.ScientistsRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('scientist');
    }
});

// /scientist/:id
ScienceMates.ScientistRoute = Ember.Route.extend({
    model: function (params) {
        return this.store.find('scientist', params.id)
    }
});

// /scientist/registration
ScienceMates.ScientistRegistrationRoute = Ember.Route.extend({
    model: function(){
        return this.store.createRecord('scientist');
    }
});


 /////////////
// Project //
////////////

// /projects
ScienceMates.ProjectsRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('project');
    }
});

// /project/add
ScienceMates.AddProjectRoute = Ember.Route.extend({
    model: function () {
        return this.store.createRecord('project');
    }
});

// /projects/:scientistID
ScienceMates.ScientistProjectsRoute = Ember.Route.extend({
    model: function( params ) {
        return this.store.find('project', params.scientistID)
    }
});
