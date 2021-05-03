console.log("pos_pre_note_template")
odoo.define('pos_note_popup_function', function (require)
{
    "use strict";
    var core = require('web.core');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var BarcodeEvents = require('barcodes.BarcodeEvents').BarcodeEvents;
    var time = require('web.time');
    var QWeb = core.qweb;
    var _t = core._t;


    var PopupNote = PopupWidget.extend({
        template: 'NotePopupWidget',
        show: function(options) {
            options = options || {};
            this._super(options);
            this.renderElement();
        },
        click_confirm: function() {
            var value = this.$('input').val();
            this.gui.close_popup();
            if (this.options.confirm) {
                this.options.confirm.call(this, value);
            }
        },
    });
    gui.define_popup({ name: 'popup_note', widget: PopupNote });


     screens.ProductScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.notes').click(function() {
                self.get_select_data();
            });
        },
        get_select_data: function() {
            var self = this;
            self.gui.show_popup('popup_note', {
                title: _t('Popup Note'),
                confirm: function() {
                alert("confirm");
                    var order = self.pos.get_order();
                    order.set_note_value(document.getElementsByName("popup_note")[0].value)
                },
                cancel: function() {},
            });
        },
        get_input_value: function() {
            return document.getElementsByName("popup_note")[0].value;
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            this.note_value = false;
            _super_order.initialize.apply(this, arguments);
        },

        set_note_value: function(note_value) {
            this.note_value = note_value;
        },
        get_note_value: function() {
//        alert("this ", this.note_value);
            return this.note_value;
        },

        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            var order = this.pos.get('selectedOrder');
            if (order) {
                json.order_note = this.note_value;
            }
            return json
        },
    });

});