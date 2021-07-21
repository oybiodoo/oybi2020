odoo.define('knowsystem.knowsystem_kanbanrender', function (require) {
"use strict";

    const KnowSystemKanbanRecord = require('knowsystem.knowsystem_kanbanrecord');
    const KanbanRenderer = require('web.KanbanRenderer');

    const KnowSystemKanbanRenderer = KanbanRenderer.extend({
        config: _.extend({}, KanbanRenderer.prototype.config, {KanbanRecord: KnowSystemKanbanRecord,}),
        /**
        * Re-write to keep selected articles when switching between pages and filters
        */
        updateSelection: function (selectedRecords) {
            _.each(this.widgets, function (widget) {
                if (typeof widget._updateRecordView === 'function') {
                    var selected = _.contains(selectedRecords, widget.id);
                    widget._updateRecordView(selected);
                }
                else {
                    _.each(widget.records, function (widg) {
                        var selected = _.contains(selectedRecords, widg.id);
                        widg._updateRecordView(selected);
                    });
                }
            });
        },

    });

    return KnowSystemKanbanRenderer;

});
