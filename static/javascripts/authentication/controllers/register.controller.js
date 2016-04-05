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
      Authentication.register(vm.email, vm.password, vm.username);
    }
  }
})();
