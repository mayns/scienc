/***********************
*   HELPERS
***********************/

(function(window, document){
    "use strict";

     window.$$ = {
        qs: function(selector, context) {
            context = context || document;
            return context.querySelector(selector);
        },
        qsa: function(selector, context) {
            context = context || document;
            return $$.toArray(context.querySelectorAll(selector));
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
            var event = new CustomEvent(type, $$.mix({}, config, defaults));
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
        mix: function(objectToMix) {
            var restObjects = [].slice.call(arguments, 1),
                toStr = Object.prototype.toString,
                arr = "[object Array]",
                key;

            restObjects.forEach(function(mixin){
                clone(objectToMix, mixin);
            });

            function clone(parent, mixin) {
                for (key in mixin) {
                    if (mixin.hasOwnProperty(key)) {
                        if (typeof mixin[key] === "object") {
                            if (typeof parent[key] !== "object") {
                                parent[key] = (toStr.call(mixin[key]) === arr) ? [] : {};
                            }
                            clone(parent[key], mixin[key]);
                        }
                        else {
                            parent[key] = mixin[key];
                        }
                    }
                }
            }

            return objectToMix;
        },
        toArray: function(collection) {
            return [].slice.call(collection);
        }
    };
})(window, document);

