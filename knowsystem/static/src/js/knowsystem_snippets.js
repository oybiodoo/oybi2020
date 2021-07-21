odoo.define('knowsystem.editor', function (require) {
"use strict";

    var options = require('web_editor.snippets.options');

    options.registry["sizing_knowsystem_x"] = options.Class.extend({
        // Option to resize snippets
        start: function () {
            var def = this._super.apply(this, arguments);

            this.containerWidth = this.$target.parent().closest("td, table, div").width();

            var self = this;
            var offset, sib_offset, target_width, sib_width;

            this.$overlay.find(".o_handle.e, .o_handle.w").removeClass("readonly");
            this.isIMG = this.$target.is("img");
            if (this.isIMG) {
                this.$overlay.find(".o_handle.w").addClass("readonly");
            }

            var $body = $(this.ownerDocument.body);
            this.$overlay.find(".o_handle").on('mousedown', function (event) {
                event.preventDefault();
                var $handle = $(this);
                var compass = false;

                _.each(['n', 's', 'e', 'w'], function (handler) {
                    if ($handle.hasClass(handler)) { compass = handler; }
                });
                if (self.isIMG) { compass = "image"; }

                $body.on("mousemove.knowsystem_width_x", function (event) {
                    event.preventDefault();
                    offset = self.$target.offset().left;
                    target_width = self.get_max_width(self.$target);
                    if (compass === 'e' && self.$target.next().offset()) {
                        sib_width = self.get_max_width(self.$target.next());
                        sib_offset = self.$target.next().offset().left;
                        self.change_width(event, self.$target, target_width, offset, true);
                        self.change_width(event, self.$target.next(), sib_width, sib_offset, false);
                    }
                    if (compass === 'w' && self.$target.prev().offset()) {
                        sib_width = self.get_max_width(self.$target.prev());
                        sib_offset = self.$target.prev().offset().left;
                        self.change_width(event, self.$target, target_width, offset, false);
                        self.change_width(event, self.$target.prev(), sib_width, sib_offset, true);
                    }
                    if (compass === 'image') {
                        self.change_width(event, self.$target, target_width, offset, true);
                    }
                });
                $body.one("mouseup", function () {
                    $body.off('.knowsystem_width_x');
                });
            });

            return def;
        },
        change_width: function (event, target, target_width, offset, grow) {
            target.css("width", grow ? (event.pageX - offset) : (offset + target_width - event.pageX));
            this.trigger_up('cover_update');
        },
        get_int_width: function (el) {
            return parseInt($(el).css("width"), 10);
        },
        get_max_width: function ($el) {
            return this.containerWidth - _.reduce(_.map($el.siblings(), this.get_int_width), function (memo, w) { return memo + w; });
        },
        onFocus: function () {
            this._super.apply(this, arguments);
            if (this.$target.is("td, th")) {
                this.$overlay.find(".o_handle.e, .o_handle.w").toggleClass("readonly", this.$target.siblings().length === 0);
            }
        },
    });

    options.registry["table_knowsystem_item"] = options.Class.extend({
        // Action to clone and delete table items
        onClone: function (options) {
            this._super.apply(this, arguments);
            if (options.isCurrent && this.$target.is("td, th")) {
                if (this.$target.siblings().length === 1) {
                    var $tr = this.$target.parent();
                    $tr.clone().empty().insertAfter($tr).append(this.$target);
                    return;
                }
                var $next = this.$target.next();
                if ($next.length && $next.text().trim() === "") {
                    $next.remove();
                    return;
                }
                var width = this.$target.width();
                var $trs = this.$target.closest("table").children("thead, tbody, tfoot").addBack().children("tr").not(this.$target.parent());
                _.each($trs.children(":nth-child(" + this.$target.index() + ")"), function (col) {
                    $(col).after($("<td/>", {style: "width: " + width + "px;"}));
                });
            }
        },
        onRemove: function () {
            this._super.apply(this, arguments);
            if (this.$target.is("td, th") && this.$target.siblings().length > 0) {
                var $trs = this.$target.closest("table").children("thead, tbody, tfoot").addBack().children("tr").not(this.$target.parent());
                if ($trs.length) {
                    var $last_tds = $trs.children(":last-child");
                    if (_.reduce($last_tds, function (memo, td) { return memo + (td.innerHTML || ""); }, "").trim() === "") {
                        $last_tds.remove();
                    } else {
                        this.$target.parent().append("<td/>");
                    }
                }
            }
        },
    });

    options.registry.BackgroundImage = options.registry.BackgroundImage.extend({
        // Adding compatibility for the outlook
        start: function () {
            this._super();
            if (this.snippets && this.snippets.split('.')[0] === "knowsystem") {
                var $table_target = this.$target.find('table:first');
                if ($table_target.length) {this.$target = $table_target;}
            }
        }
    });

});
