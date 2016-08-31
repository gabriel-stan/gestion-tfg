/**
* editDepartamento
* @namespace gestfg.departamentos.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.departamentos.directives')
    .directive('editDepartamento', editDepartamento);

  /**
  * @namespace editDepartamento
  */
  function editDepartamento() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.departamentos.directives.editDepartamento
    */
    var directive = {
      controller: 'NewDepartamentoController',
      controllerAs: 'vm',
      scope: {
        departamento: '='
      },
      restrict: 'E',
      templateUrl: '/static/templates/departamentos/edit-departamento.html'
    };

    return directive;
  }
})();
