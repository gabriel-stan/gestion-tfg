(function () {
  'use strict';

  angular
    .module('gestfg.events', [
      'gestfg.events.controllers',
      'gestfg.events.directives',
      'gestfg.events.services'
    ]);

  angular
    .module('gestfg.events.controllers', []);

  angular
    .module('gestfg.events.directives', ['ngDialog']);

  angular
    .module('gestfg.events.services', []);
})();
