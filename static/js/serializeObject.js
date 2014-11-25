/***********************
 *   SERIALIZE OBJECT
 ***********************/

/**
 * jQuery serializeObject
 * @copyright 2014, macek <paulmacek@gmail.com>
 * @link https://github.com/macek/jquery-serialize-object
 * @license BSD
 * @version 2.3.0
 */

(function ($) {
    "use strict";

    var patterns = {
        validate: /^[a-z][a-z0-9_]*(?:\[(?:\d*|[a-z0-9_]+)\])*$/i,
        key:      /[a-z0-9_]+|(?=\[\])/gi,
        push:     /^$/,
        fixed:    /^\d+$/,
        named:    /^[a-z0-9_]+$/i
    };


    function FormSerializer(root, options) {

        // Private variables
        var options = $.mix({}, FormSerializer.defaults.options, options);
        this._data = {};
        this._pushes = {};
        this.root = root;
        this.attr = options.attr;
        this.addBlankFields = options.addBlankFields;
    }
    FormSerializer.prototype = {

        // Private API

        constructor: FormSerializer,
        init: function () {
            return this.addPairs(this.serializeArray(this.attr)).serialize();
        },
        _build: function (base, key, value) {
//          Если не проверять value на null,
//          то пустой массив не будет создан
            if (value === null && Array.isArray(base)) {
                return base;
            }
            else if (value === null) {
                base[key] = '';
                return base;
            }
            base[key] = value;
            return base;
        },
        _makeObject: function (root, value) {
            var keys = root.match(patterns.key), k, idx;
            // nest, nest, ..., nest
            while ((k = keys.pop()) !== undefined) {
                // foo[]
                if (patterns.push.test(k)) {
//              Здесь условие нужно, чтобы предотвратить
//              инкремент индекса массива, если значение null,
//              то пропускаем increment

                    if (value !== null) {
                        idx = this._incrementPush(root.replace(/\[\]$/, ''));
                    }
                    value = this._build([], idx, value);
                }

                // foo[n]
                else if (patterns.fixed.test(k)) {
                    value = this._build([], k, value);
                }

                // foo; foo[bar]
                else if (patterns.named.test(k)) {
                    value = this._build({}, k, value);
                }
            }

            return value;
        },
        _incrementPush: function(key) {
            if (this._pushes[key] === undefined) {
                this._pushes[key] = 0;
            }
            return this._pushes[key]++;
        },

        // Public API

        addPair: function(pair) {
            var self = this;
            if (Array.isArray(pair)) {
                pair.forEach(function(pair){
                    self.addPair(pair);
                });
                return;
            }
            if (!patterns.validate.test(pair.name)) return self;
            var obj = self._makeObject(pair.name, pair.value);
            self._data = $.mix({}, self._data, obj);
            return self;
        },
        addPairs: function (pairs) {
            if (!Array.isArray(pairs)) {
                throw new Error("formSerializer.addPairs expects an Array");
            }
            for (var i=0, len=pairs.length; i<len; i++) {
                this.addPair(pairs[i]);
            }
            return this;
        },
        serialize: function() {
            return this._data;
        },
        serializeJSON: function() {
            return JSON.stringify(this.serialize());
        },
        serializeArray: function() {
            var self = this;
            var root = self.root;
            var attr = self.attr;
            var rcheckableType = (/^(?:checkbox|radio)$/i);
            var counter = 0;
            var r20 = /%20/g,
                rbracket = /\[\]$/,
                rCRLF = /\r?\n/g,
                rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
                rsubmittable = /^(?:input|select|textarea|keygen)/i;

            //  Получить элементы с аттрибутом

            var elements = [].slice.call(root.querySelectorAll('['+attr+']'));

            return elements
                .filter(function (field) {

                    var type = field.type;
                    // Фильтруем disabled, submit, button, image, reset, file
                    // Оставляем input, select, textarea, keygen
                    // Если стоит флаг addBlankFields, то checkboxes и select-multiple
                    // будут иметь пустой массив, если значения не выбраны
                    // иначе просто не попадают в JSON
                    if (self.addBlankFields) {
                        return field.getAttribute(attr) && !(field.disabled) &&
                            rsubmittable.test(field.nodeName) && !rsubmitterTypes.test(type) &&
                            ( (field.checked && field.type === 'radio' || field.type === 'checkbox' ) || !rcheckableType.test(type) );
                    }
                    return field.getAttribute(attr) && !(field.disabled) &&
                            rsubmittable.test( field.nodeName ) && !rsubmitterTypes.test( type ) &&
                                ( field.checked || !rcheckableType.test( type ) ) && (field.value !== "");
                })
                .map(function (field) {
                    //  Фильтруем нечекнутые чекбоксы и радио кнопки
                    var val = field.value;
                    if (self.addBlankFields) {
                        if ((field.checked === false && field.type === 'checkbox') || (field.type === 'select-multiple' && val === null)) {
                            return {
                                name: field.getAttribute(attr),
                                value: null
                            };
                        }
                    }
                    if (val === null) {
                        return null;
                    }
                    else if (Array.isArray(val)) {
                        return val.map(function (val) {
                            return {
                                name: field.getAttribute(attr),
                                value: val.replace(rCRLF, "\r\n")
                            };
                        });
                    }
                    else {
                        return {
                            name: field.getAttribute(attr),
                            value: val.replace(rCRLF, "\r\n")
                        };
                    }
                });
        }
    };


    FormSerializer.patterns = patterns;

    FormSerializer.defaults = {
        options: {
            attr: 'name',
            addBlankFields: false
        }
    };

    $.serializeObject = FormSerializer.serializeObject = function serializeObject(options) {
        if (typeof options === "string") {
            options = {
                attr: options
            };
        }
        return new FormSerializer(this, options).init();
    };

    $.serializeArray =  FormSerializer.serializeJSON = function serializeJSON(options) {
        return JSON.stringify(new FormSerializer(this, options).init());
    };


})(window.$);