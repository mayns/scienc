/***********************
*   HELPERS
***********************/

(function(window, document){
    "use strict";

     window.$ = {
        qs: function(selector, context) {
            context = context || document;
            return context.querySelector(selector);
        },
        qsa: function(selector, context) {
            context = context || document;
            return $.toArray(context.querySelectorAll(selector));
        },
        on: function(el, type, callback, useCapture) {
            el.addEventListener(type, callback, Boolean(useCapture));
        },
        off: function(el, type, callback, useCapture) {
            el.removeEventListener(type, callback, Boolean(useCapture));
        },
        trigger: function(el, type, config) {
            var defaults = {
                bubbles: true,
                cancelable: true
            };
            var event = new CustomEvent(type, $.mix({}, config, defaults));
            el.dispatchEvent(event);
        },
        delegate: function(el, type, selector, callback) {
            el.addEventListener(type, function(e){
                var target = e.target;

                while(target != el) {
                    if (target.matches(selector)) {
                        callback.call(target, e);
                    }
                    target = target.parentNode;
                }
            });
        },
        mix: function(objetToMix) {
            var restObjects = [].slice.call(arguments, 1),
                key;

            restObjects.forEach(function(mixin){
                for (key in mixin) {
                    if (mixin.hasOwnProperty(key)) {
                        objetToMix[key] = mixin[key];
                    }
                }
            });

            return objetToMix;
        },
        toArray: function(collection) {
            return [].slice.call(collection);
        }
    };
})(window, document);

