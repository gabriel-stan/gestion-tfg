/**
* tfgsTabla
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('tfgsTabla', tfgsTabla);

  /**
  * @namespace tfgsTabla
  */
  function tfgsTabla() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.tfgsTabla
    */
    var directive = {
      // controller: 'NewTfgController',
      // controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/templates/tfgs/tfgs-tabla.html'
    };

    return directive;
  }
})();
