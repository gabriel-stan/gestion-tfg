/**
* newUserModal
* @namespace gestfg.users.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.directives')
    .directive('newUserModal', newUserModal);

  /**
  * @namespace newUserModal
  */
  function newUserModal() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.users.directives.newUserModal
    */
    var directive = {
      controller: 'NewUserController',
      controllerAs: 'vm',
      restrict: 'E',
      scope: {
        user: '='
      },
      templateUrl: '/static/templates/users/new-user-modal.html'
    };

    return directive;
  }
})();
