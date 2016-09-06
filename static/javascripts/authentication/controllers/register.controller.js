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
  function RegisterController($location, $scope, $routeParams, Authentication) {
    var registerCtrl = this;

    registerCtrl.register = register;
    registerCtrl.recoverPassword = recoverPassword;
    registerCtrl.resetPassword = resetPassword;

    $scope.register = register;
    $scope.recoverPassword = recoverPassword;
    $scope.resetPassword = resetPassword;

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
        preAction();
        Authentication.resetPassword(registerCtrl.password, registerCtrl.repassword, uidb64, token).finally(postAction);
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
      preAction();
      Authentication.recoverPassword(registerCtrl.email).finally(postAction);
    }

    /**
    * @name register
    * @desc Register a new user
    * @memberOf gestfg.authentication.controllers.RegisterController
    */
    function register() {
      preAction();
      Authentication.register(registerCtrl.email, registerCtrl.dni, registerCtrl.first_name, registerCtrl.last_name);
      postAction();
    }

    function preAction(){
      $scope.loading = true;
    }

    function postAction(){
      $scope.loading = false;
    }
  }
})();
