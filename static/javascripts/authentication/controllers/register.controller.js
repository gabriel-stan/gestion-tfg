/**
* Register controller
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication) {
    var registerCtrl = this;

    registerCtrl.register = register;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
    * @name register
    * @desc Register a new user
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function register() {
      Authentication.register(registerCtrl.email, registerCtrl.password, registerCtrl.first_name, registerCtrl.last_name);
    }
  }
})();
