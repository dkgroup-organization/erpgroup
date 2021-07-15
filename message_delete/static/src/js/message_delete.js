odoo.define('message_delete.message_delete', function (require) {

    var core = require('web.core');
    var data = require('web.data');
    var _t = core._t;
    var chatThread = require('mail.widget.Thread');

    chatThread.include({
        events: _.extend({}, chatThread.prototype.events, {
            'click .fa-trash': '_onMessageDelete',
        }),
        _onMessageDelete: function (event) {
            // The method to proceed message unlink
            event.stopPropagation();
            if (! confirm(_t("Do you really want delete this message?"))) { return false; }
            var self = this;
            var messageId = parseInt(event.target.dataset['messageId'], 10),
                cTX = {"message_delete": true};
            this._rpc({
                model: "mail.message",
                method: "unlink",
                args: [[messageId]],
                context: cTX,
            }).then(function (res) {
                location.reload();
            });
        }
    });
});
