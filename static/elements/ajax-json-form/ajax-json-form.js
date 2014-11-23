(function(window, document, $) {
    "use strict";

    /***********************
    *   ELEMENT
    ***********************/


    var proto = Object.create(window.HTMLFormElement.prototype);

    proto.createdCallback = function() {
        this.addEventListener('submit', function(e){
            e.preventDefault();
            var jsonData = this.serializeObject(),
                formData = new FormData(),
                xhr = new XMLHttpRequest();

            formData.append('data', JSON.stringify(jsonData));
            xhr.open('POST', this.action, true);
            xhr.send(formData);
            xhr.onload = function() {
                console.log('Data loaded');
            }
        });
    };

    proto.serializeObject = function() {
        return $.serializeObject.call(this);
    };

    document.registerElement('ajax-json-form', {
        prototype: proto,
        extends: 'form'
    });

})(window, document, $);