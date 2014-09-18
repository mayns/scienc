/**
 * Created by mayns on 25/07/14.
 */

window.ScienceMates = Ember.Application.create();

//ScienceMates.ApplicationAdapter = DS.FixtureAdapter;

ScienceMates.ApplicationAdapter = DS.RESTAdapter.extend({
    namespace: 'api',
    findAll: function (store, type) {
        return this._super(store, type);
    },
    find: function (store, type) {
        return this._super(store, type);
    }
});
