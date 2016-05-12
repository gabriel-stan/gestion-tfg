/**
* NavbarRight
* @namespace gestfg.layout.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.directives')
    .directive('navbarRight', navbarRight);

  /**
  * @namespace NavbarRight
  */
  function navbarRight() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.layout.directives.NavbarRight
    */
    var directive = {
      controller: 'NavbarController',
      controllerAs: 'navCtrl',
      restrict: 'E',
      templateUrl: '/static/templates/layout/navbar-right.html'
    };

    return directive;
  }
})();
