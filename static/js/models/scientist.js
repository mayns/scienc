/**
 * Created by mayns on 25/07/14.
 */

ScienceMates.Scientist = DS.Model.extend({
    first_name: DS.attr('string'),
    middle_name: DS.attr('string'),
    last_name: DS.attr('string'),
    location_country: DS.attr('string'),
    location_city: DS.attr('string'),
    image: DS.attr('string'),
    university: DS.attr('string'),
    faculty: DS.attr('string'),
    chair: DS.attr('string'),
    email: DS.attr('string'),
    password: DS.attr('string'),

    full_name: function() {
        return this.get('first_name') + ' ' + this.get('middle_name') + ' ' + this.get('last_name');
    }.property('first_name', 'middle_name', 'last_name')

});