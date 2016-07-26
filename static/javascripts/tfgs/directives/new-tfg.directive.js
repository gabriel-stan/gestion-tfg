/**
* newTfg
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('newTfg', newTfg);

  /**
  * @namespace newTfg
  */
  function newTfg() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.newTfg
    */
    var directive = {
      controller: 'NewTfgController',
      controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/templates/tfgs/new-tfg.html'
    };

    return directive;
  }
})();
