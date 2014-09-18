/**
 * Created by mayns on 27/07/14.
 */

ScienceMates.ScientistsController = Ember.ArrayController.extend({
    actions: {
        remove: function(sci_id) {
            var store = this.store;
            store.find('scientist', sci_id).then(function (scientist) {
                scientist.deleteRecord();
                scientist.get('isDeleted'); // => true
                scientist.save(); // => DELETE to /posts/1
//            var scientist = this.store.find('scientist', sci_id);
//            var store = this.store;
//            console.log(store);
//            scientist.then(function (item) {
//                item.destroyRecord();
//                store.commit();
//            });
            });
        }
    }
});