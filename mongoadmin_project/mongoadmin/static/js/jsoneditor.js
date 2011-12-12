(function($) {

$.extend({
    keys: function(obj){
        var a = [];
        $.each(obj, function(k){ a.push(k) });
        return a;
    }
})


$.fn.JSONEditor = function(options) {
    var defaults = {
        depth: 4,
        idPrefix: 'json',
        indent: 4
    };
    var options = $.extend(defaults, options);


    return this.each(function() {
        var textarea = $(this);


        var parent = $('#'+options.idPrefix);
        if (!parent.length) {
            parent = $('<div>').attr('id', options.idPrefix).insertAfter(textarea);
        }
        var rootObj = null;
        var focus = null;

        function renderRoot() {
            $(parent).html('');
            textarea.removeClass('error');
            if (rootObj != null) {
                render(parent, rootObj, options.depth-1, options.idPrefix);
            }
        }

        function render(el, obj, depth, idPrefix) {

            if (el == parent) {
                textarea.val(JSON.stringify(rootObj, null, options.indent));
            }

            if (obj.constructor == Array || obj.constructor == Object) {
                var keys = $.keys(obj).sort();
                console.log(obj);
                for (var i=0;i<=keys.length;i++) {
                    (function() {
                        var id = idPrefix + '_' + i;
                        var key;
                        if (i == keys.length) {
                            if (obj.constructor == Array) {
                                key = ''+i;
                            } else {
                                key = '';
                            }
                        } else { 
                            key = keys[i];
                        }
                            
                        var child = (i == keys.length) ? undefined : obj[key];
                        var div = $('<div class="input-prepend">').attr('id', id);
                        var valueEl = $('<input class="xxlarge value" type="text">').val(JSON.stringify(child)).attr('id', id+'_value');
                        var prevKey;
                        var prevValue;

                        var keyEl;
                        if (obj.constructor == Object) {
                            keyEl = $('<input class="add-on key" type="text">').val(key).attr('id', id+'_key');
                            (function(theKey) {
                                keyEl.focus(function() {
                                    prevKey = $(this).val();
                                    focus = $(this);
                                }).blur(function() {
                                    focus = null;
                                }).change(function() { 
                                    // TODO: warning if key exists?
                                    var val = $(this).val();
                                    if (val == '') {
                                        valueEl.attr('tabIndex', -1);
                                    } else {
                                        valueEl.removeAttr('tabIndex');
                                    }
                                    if (prevKey != val) {
                                        obj[val] = obj[prevKey];
                                        delete obj[prevKey];
                                    }
                                    if ($(valueEl).val() == '') {
                                        $(valueEl).focus();
                                        return;
                                    } else {
                                        renderRoot();
                                        var parts = $(this).attr('id').split('_');
                                        parts.splice(parts.length-2, 2);
console.log(parts);
                                        var searchDivs;
                                        if (parts.length == 1) {
                                            searchDivs = $('#' + options.idPrefix + '>div');
                                        } else {
                                            searchDivs = $('#' + parts.join('_') + '_indent>div');
                                        }
                                        searchDivs.each(function() {
                                            if ($(this).find('input.key').val() == val) {
                                                $(this).find('input.value').select();
                                            }
                                        });
                                    }
                                });
                            })(key);
                        } else {
                            keyEl = $('<span class="add-on">').text(key);
                        }
                        if (''+key == '') {
                            valueEl.attr('tabIndex', -1);
                        }

                        valueEl.focus(function(ev) {
                            prevValue = $(this).val();
                            if (obj.constructor == Object && $(keyEl).val() == '') {
                                $(keyEl).focus();
                            }
                            focus = $(this);
                        }).blur(function() {
                            focus = null;

                            var val = $(this).val();
                            if ((obj.constructor == Object && $(keyEl).val() == '') || ((obj.constructor == Array || val.length) && val == prevValue)) {
                                return;
                            }

                            val = val.trim();

                            if (val.length > 0) {
                                if (val != "false" && val != "true" && val != 'null') {
                                    if (!val.trim().match(/^["0-9-{[]/)) {
                                        val = '"' + val.replace('"', '\\"') + '"';
                                    }
                                }
                            }

                            try {
                                val = $.parseJSON(val);
                            } catch(e) {
                                $(this).addClass('error');
                                return;
                            }

                            var theKey = (obj.constructor == Object) ? $(keyEl).val() : $(keyEl).text();
                            obj[theKey] = val;
                            var parts = $(this).attr('id').split('_');
                            parts[parts.length-2] = parseInt(parts[parts.length-2], 10)+1
                            if (obj.constructor == Object)
                                parts[parts.length-1] = "key";
                            else
                                parts[parts.length-1] = "value";
                            renderRoot();
                            $('#' + parts.join("_")).select();
                        });

                        div.append(keyEl).append(valueEl);
                        div.append($('<a href="#" class="delete">&#10006;</a>').click(function(ev) {
                            if (obj.constructor == Object) {
                                delete obj[key];
                            } else {
                                obj.splice(key, 1);
                            }
                            renderRoot();
                            ev.preventDefault();
                        }));
                        el.append(div);

                        if (depth > 0 && child && (child.constructor == Array || child.constructor == Object) && key != '_id') {
                            var indent = $('<div class="indent">').attr('id', id+'_indent');
                            el.append(indent);
                            render(indent, child, depth-1, id);
                        }
                    })();
                }
            }
        }

        loadRoot();

        function loadRoot() {
            try {
                rootObj = $.parseJSON(textarea.val());
            } catch(e) {
                textarea.addClass('error');
                return;
            }
            renderRoot();
        }

        textarea.change(function() {
            loadRoot();
        });
    });
}

})(jQuery);
