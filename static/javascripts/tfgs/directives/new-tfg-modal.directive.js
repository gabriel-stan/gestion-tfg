/**
* newTfg
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('newTfgModal', newTfgModal);

  /**
  * @namespace newTfgModal
  */
  function newTfgModal() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.newTfgModal
    */
    var directive = {
      controller: 'NewTfgController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        tfg: '='
      },
      templateUrl: '/static/templates/tfgs/new-tfg-modal.html'
    };

    return directive;
  }
})();
