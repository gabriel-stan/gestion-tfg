/**
* newUser
* @namespace gestfg.users.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.directives')
    .directive('newUser', newUser);

  /**
  * @namespace newUser
  */
  function newUser() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.users.directives.newUser
    */
    var directive = {
      controller: 'NewUserController',
      controllerAs: 'vm',
      restrict: 'E',
      templateUrl: '/static/templates/users/new-user.html'
    };

    return directive;
  }
})();
