/**
* Users
* @namespace gestfg.users.directives
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.directives')
    .directive('users', users);

  /**
  * @namespace Users
  */
  function users() {
    /**
    * @name directive
    * @desc The directive to be returned
    * @memberOf gestfg.users.directives.Users
    */
    var directive = {
      controller: 'UsersController',
      controllerAs: 'usersCtrl',
      restrict: 'E',
      scope: {
        users: '='
      },
      link: function (scope, element, attr, controller){
        // alert("directive loading");
        // scope.loadUsers();
        controller.loadUsers()
      },
      templateUrl: '/static/templates/users/users.html'
    };

    return directive;
  }
})();
