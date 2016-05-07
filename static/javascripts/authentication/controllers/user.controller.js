/**
* User controller
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('UserController', UserController);

  UserController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace UserController
  */
  function UserController($location, $scope, Authentication) {
    var userCtrl = this;

    userCtrl.isAuthenticated = isAuthenticated;
    userCtrl.isAdmin = isAdmin;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.authentication.controllers.UserController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      // if (Authentication.isAuthenticated()) {
      //   $location.url('/');
      // }
    }

    /**
    * @name isAuthenticated
    * @desc Check if user is authenticated
    * @memberOf gestfg.authentication.controllers.UserController
    */
    function isAuthenticated() {
      return Authentication.isAuthenticated()
    }

    /**
    * @name isAdmin
    * @desc Check if user is admin
    * @memberOf gestfg.authentication.controllers.UserController
    */
    function isAdmin() {
      return Authentication.isAdmin()
    }
  }
})();
