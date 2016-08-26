(function () {
    'use strict';

    angular
      .module('gestfg', [
        'gestfg.config',
        'gestfg.routes',
        'gestfg.authentication',
        'gestfg.layout',
        'gestfg.events',
        'gestfg.users',
        'gestfg.tfgs',
        'gestfg.departamentos',
        'gestfg.comisiones',
        'gestfg.utils',
        'ngSanitize'
      ]);

    angular
      .module('gestfg.routes', ['ngRoute']);

    angular
        .module('gestfg.config', []);

    angular
        .module('gestfg')
        .run(run);

    run.$inject = ['$http'];

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';

        //initialize material theme
        // $.material.init();
    }

  })();
