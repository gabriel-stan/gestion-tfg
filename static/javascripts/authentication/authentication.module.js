(function () {
  'use strict';

  angular
    .module('gestfg.authentication', [
      'gestfg.authentication.controllers',
      'gestfg.authentication.services'
    ]);

  angular
    .module('gestfg.authentication.controllers', []);

  angular
    .module('gestfg.authentication.services', ['ngCookies']);
})();
