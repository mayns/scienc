/**
 * jQuery serializeObject
 * @copyright 2014, macek <paulmacek@gmail.com>
 * @link https://github.com/macek/jquery-serialize-object
 * @license BSD
 * @version 2.3.0
 */
"use strict";

window.For (function () {

    var patterns = {
        validate: /^[a-z][a-z0-9_]*(?:\[(?:\d*|[a-z0-9_]+)\])*$/i,
        key:      /[a-z0-9_]+|(?=\[\])/gi,
        push:     /^$/,
        fixed:    /^\d+$/,
        named:    /^[a-z0-9_]+$/i
    };


    function FormSerializer($root, options) {

        // Private variables
        var options = $.extend(true, FormSerializer.defaults.options, options);
        this._data = {};
        this._pushes = {};
        this.$root = $root;
        this.attr = options.attr || 'name';
        this.addBlankFields = options.addBlankFields || false;
    }
    FormSerializer.prototype = {

        // Private API

        constructor: FormSerializer,
        init: function () {
            return this.
                addPairs(this.serializeArray(this.attr)).
                serialize();
        },
        _build: function (base, key, value) {
//          Если не проверять value на null,
//          то пустой массив не будет создан
            if (value === null && $.isArray(base)) {
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
            if (!patterns.validate.test(pair.name)) return self;
            var obj = self._makeObject(pair.name, pair.value);
            self._data = $.extend(true, self._data, obj);
            return self;
        },
        addPairs: function (pairs) {
            if (!$.isArray(pairs)) {
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
            var $root = this.$root;
            var attr = this.attr;
            var rcheckableType = (/^(?:checkbox|radio)$/i);
            var counter = 0;
            var r20 = /%20/g,
                rbracket = /\[\]$/,
                rCRLF = /\r?\n/g,
                rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
                rsubmittable = /^(?:input|select|textarea|keygen)/i;

            //  Получить элементы с аттрибутом

            var elements = $root.find('['+attr+']');

            return elements
                .filter(function () {

                    var type = this.type;
                    // Фильтруем disabled, submit, button, image, reset, file
                    // Оставляем input, select, textarea, keygen
                    // Если стоит флаг addBlankFields, то checkboxes и select-multiple
                    // будут иметь пустой массив, если значения не выбраны
                    // иначе просто не попадают в JSON
                    if (self.addBlankFields) {
                        return this.getAttribute(attr) && !$(this).is(":disabled") &&
                            rsubmittable.test(this.nodeName) && !rsubmitterTypes.test(type) &&
                            ( (this.checked && this.type === 'radio' || this.type === 'checkbox' ) || !rcheckableType.test(type) );
                    }
                    return this.getAttribute(attr) && !$( this ).is( ":disabled" ) &&
                        rsubmittable.test( this.nodeName ) && !rsubmitterTypes.test( type ) &&
                        ( this.checked || !rcheckableType.test( type ) );

                })
                .map(function (i, elem) {
                    //  Фильтруем нечекнутые чекбоксы и радио кнопки
                    var val = $(this).val();
                    if (self.addBlankFields) {
                        if ((this.checked === false && this.type === 'checkbox') || (this.type === 'select-multiple' && val === null)) {
                            return {
                                name: elem.getAttribute(attr),
                                value: null
                            };
                        }
                    }
                    if (val === null) {
                        return null;
                    }
                    else if ($.isArray(val)) {
                        return $.map(val, function (val) {
                            return {
                                name: elem.getAttribute(attr),
                                value: val.replace(rCRLF, "\r\n")
                            };
                        });
                    }
                    else {
                        return {
                            name: elem.getAttribute(attr),
                            value: val.replace(rCRLF, "\r\n")
                        };
                    }
//                  Просто получаем элементы без $ обертки
            }).get();
        }
    };


    FormSerializer.patterns = patterns;

    FormSerializer.serializeObject = function serializeObject(options) {
        if (this.length > 1) {
            return new Error("jquery-serialize-object can only serialize one form at a time");
        }
        if (typeof options === "string") {
            options = {
                attr: options
            };
        }
        return new FormSerializer(this, options).init();
    };

    FormSerializer.serializeJSON = function serializeJSON(options) {
        if (this.length > 1) {
            return new Error("jquery-serialize-object can only serialize one form at a time");
        }
        return JSON.stringify(new FormSerializer(this, options).init());
    };
    FormSerializer.defaults = {
        options: {
            attr: 'name',
            addBlankFields: true
        }
    };
    if (typeof $.fn !== "undefined") {
        $.fn.serializeObject = FormSerializer.serializeObject;
        $.fn.serializeJSON   = FormSerializer.serializeJSON;
    }

    return FormSerializer;
})();