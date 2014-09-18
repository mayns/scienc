/**
 * Created by mayns on 13/09/14.
 */

ScienceMates.AddProjectController = Ember.ObjectController.extend({
    actions: {
        save: function(){
            console.log('in save');
            var project = this.store.createRecord('project', {
//                scientistID: this.get('scientistID'),
                title: this.get('title'),
                objective: this.get('objective'),
                description: this.get('description'),
                results: this.get('results'),
                team: this.get('team')

            });
            project.save().then(function(response){
            }, function(response){
                console.log(response);
                if(response.error){
                    project.deleteRecord();
                }
            });
            this.transitionToRoute('projects');
        }
    }
});