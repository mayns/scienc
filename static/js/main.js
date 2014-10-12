/**
 * Created by andrey on 13.10.14.
 */
require.config({
    baseUrl: '/static/js'
});

require(['app'], function(App){
    App.start();
});