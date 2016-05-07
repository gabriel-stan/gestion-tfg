/**
* NavbarController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication) {
    var navCtrl = this;

    navCtrl.logout = logout;

    /**
    * @name logout
    * @desc Log the user out
    * @memberOf gestfg.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout();
    }
  }
})();
