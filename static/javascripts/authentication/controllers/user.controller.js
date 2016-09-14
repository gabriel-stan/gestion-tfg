/**
* User controller
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('UserController', UserController);

  UserController.$inject = ['$location', '$scope', 'Authentication', 'Users'];

  /**
  * @namespace UserController
  */
  function UserController($location, $scope, Authentication, Users) {
    var userCtrl = this;

    userCtrl.isAuthenticated = isAuthenticated;
    userCtrl.isAdmin = isAdmin;
    userCtrl.user = Authentication.getAuthenticatedAccount();
    userCtrl.getAuthenticatedAccount = getAuthenticatedAccount;
    userCtrl.loadUserData = loadUserData;

    userCtrl.userData = new Object();

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

    function getAuthenticatedAccount() {
      return Authentication.getAuthenticatedAccount();
    }

    function loadUserData() {

      if(isAuthenticated()){
        Users.get(userCtrl.user.data.email).then(getSuccessFn, getErrorFn);

        function getSuccessFn(data, status, headers, config) {
          userCtrl.userData = data.data.data[0];
        }

        function getErrorFn(data, status, headers, config) {
          console.log("Error al obtener los datos del usuario");
        }

      }
    }
  }
})();
