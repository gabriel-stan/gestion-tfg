/**
* NavbarController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', '$location', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, $location, Authentication) {
    var navCtrl = this;

    navCtrl.logout = logout;
    navCtrl.isDashboard = isDashboard;

    function isDashboard(){
      if ($location.path().match("^/dashboard")) {
        return true;
      } else {
        return false;
      }
    }

    /**
    * @name logout
    * @desc Log the user out
    * @memberOf gestfg.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout();
    }

    $scope.getClass = function (path) {
      if(path == 'home' && $location.path() == '/'){
        return 'active';
      }
      return ($location.path().substr(0, path.length) === path) ? 'active' : '';
    }

  }
})();
