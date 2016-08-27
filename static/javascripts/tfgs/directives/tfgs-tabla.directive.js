/**
* tfgsAsigTabla
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('tfgsAsigTabla', tfgsAsigTabla);

  /**
  * @namespace tfgsAsigTabla
  */
  function tfgsAsigTabla() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.tfgsAsigTabla
    */
    var directive = {
      // controller: 'TfgsController',
      // controllerAs: 'tfgsCtrl',
      restrict: 'E',
      templateUrl: '/static/templates/tfgs/tfgs-asig-tabla.html'
    };

    return directive;
  }
})();
