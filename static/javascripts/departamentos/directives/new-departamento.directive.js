/**
* newDepartamento
* @namespace gestfg.departamentos.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.directives')
    .directive('newDepartamento', newDepartamento);

  /**
  * @namespace newDepartamento
  */
  function newDepartamento() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.departamentos.directives.newDepartamento
    */
    var directive = {
      controller: 'NewDepartamentoController',
      controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/templates/departamentos/new-departamento.html'
    };

    return directive;
  }
})();
