odoo.define('od_sale.popup', function (require) {
    "use strict";
    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');

    var PopupWidget = Widget.extend({
        events: {
            'click .show-popup': '_onShowPopup',
        },
        _onShowPopup: function () {
            var dialog = new Dialog(this, {
                title: "Custom Popup",
                size: 'medium',
                buttons: [
                    {text: "Close", close: true}
                ],
                $content: $("<p>This is a custom popup content!</p>")
            });
            dialog.open();
        },
    });

    return PopupWidget;
});
