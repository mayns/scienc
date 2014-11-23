(function(window, document) {
    "use strict";

    /***********************
    *   ELEMENT
    ***********************/


    var proto = Object.create(window.HTMLFormElement);
    proto.createdCallback = function() {
        this.addEventListener('submit', function(){

        });
    };

    document.registerElement('ajax-json-form', {
        prototype: proto,
        extends: 'form'
    });

})(window, document);