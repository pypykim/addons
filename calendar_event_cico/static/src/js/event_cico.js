openerp.calendar_event_cico = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.calendar_event_cico.Check = instance.Widget.extend({
        start: function () {
            console.log("calendar_event_cico.Check() executed.");
        },
    });

    instance.web.client_actions.add(
        'calendar_event_cico_check', 'instance.calendar_event_cico.Check');
}