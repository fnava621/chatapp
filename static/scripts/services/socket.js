'use strict';

angular.module('chatWebApp')
    .factory('socket', function (socketFactory) {
        var socket = socketFactory({
            ioSocket: io.connect('/chat')
        });
        socket.forward('error');
        return socket;
    });