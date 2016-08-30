/**
* Register controller
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', '$routeParams', 'Authentication'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $routeParams, $scope, Authentication) {
    var registerCtrl = this;

    registerCtrl.register = register;
    registerCtrl.recoverPassword = recoverPassword;
    registerCtrl.resetPassword = resetPassword;

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
    * @name resetPassword
    * @desc resetPassword of a user
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function resetPassword() {
      //var token = $location.path().split("/")[1]||"";
      //var token = $routeParams.token;

      if(registerCtrl.password == registerCtrl.repassword){
        registerCtrl.error = false;
        var token = $location.search().token;
        var uidb64 = $location.search().uidb64;
        Authentication.resetPassword(registerCtrl.password, registerCtrl.repassword, uidb64, token);
      } else {
        registerCtrl.error = true;
      }
    }

    /**
    * @name recoverPassword
    * @desc recoverPassword of a user
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function recoverPassword() {
      Authentication.recoverPassword(registerCtrl.email);
    }

    /**
    * @name register
    * @desc Register a new user
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function register() {
      Authentication.register(registerCtrl.email, registerCtrl.dni, registerCtrl.first_name, registerCtrl.last_name);
    }
  }
})();
