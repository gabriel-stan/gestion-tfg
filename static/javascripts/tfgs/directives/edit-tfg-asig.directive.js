/**
* editTfgAsig
* @namespace gestfg.tfgs.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.tfgs.directives')
    .directive('editTfgAsig', editTfgAsig);

  /**
  * @namespace editTfgAsig
  */
  function editTfgAsig() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.tfgs.directives.editTfg
    */
    var directive = {
      controller: 'NewTfgController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        tfg: '='
      },
      templateUrl: '/static/templates/tfgs/edit-tfg-asig.html'
    };

    return directive;
  }
})();
