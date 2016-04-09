/**
* Register controller
* @namespace gestfg.authentication.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Authentication', '$http'];

  activate();

  /**
  * @name activate
  * @desc Actions to be performed when this controller is instantiated
  * @memberOf thinkster.authentication.controllers.RegisterController
  */
  function activate() {
    // If the user is authenticated, they should not be here.
    if (Authentication.isAuthenticated()) {
      $location.url('/');
    }
  }

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Authentication , $http) {
    var vm = this;

    vm.register = register;

    /**
    * @name register
    * @desc Register a new user
    * @memberOf thinkster.authentication.controllers.RegisterController
    */
    function register() {
      Authentication.register(vm.email, vm.password, vm.first_name, vm.last_name);
    }
  }
})();
