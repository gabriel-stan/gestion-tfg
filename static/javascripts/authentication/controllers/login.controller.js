/**
* LoginController
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace LoginController
  */
  function LoginController($location, $scope, Authentication) {
    var loginCtrl = this;

    loginCtrl.login = login;
    $scope.login = login;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.authentication.controllers.LoginController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name login
    * @desc Log the user in
    * @memberOf gestfg.authentication.controllers.LoginController
    */
    function login() {
      preAction();
      Authentication.login(loginCtrl.email, loginCtrl.password).finally(postAction);
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }
  }
})();
