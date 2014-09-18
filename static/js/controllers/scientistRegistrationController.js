/**
 * Created by mayns on 27/07/14.
 */

ScienceMates.ScientistRegistrationController = Ember.ObjectController.extend({
    actions: {
        save: function(){

            var scientist = this.store.createRecord('scientist', {
                first_name: this.get('first_name'),
                middle_name: this.get('middle_name'),
                last_name: this.get('last_name'),
                location_country: this.get('location_country'),
                location_city: this.get('location_city'),
                image: this.get('image'),
                university: this.get('university'),
                faculty: this.get('faculty'),
                chair: this.get('chair'),
                email: this.get('email'),
                password: this.get('password')

            });
            scientist.save();
            this.transitionToRoute('scientists');
        }
    }
});