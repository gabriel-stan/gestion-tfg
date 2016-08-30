/**
* DashSidebarController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('DashSidebarController', DashSidebarController);

  DashSidebarController.$inject = ['$scope', '$location', 'Authentication'];

  /**
  * @namespace DashSidebarController
  */
  function DashSidebarController($scope, $location, Authentication) {
    var sidebarCtrl = this;

    sidebarCtrl.logout = logout;
    sidebarCtrl.isDashboard = isDashboard;

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
      //return ($location.path().substr(0, path.length) === path) ? 'active' : '';
      // var asdad = $location.path().substr(0, $location.path().substring($location.path().lastIndexOf("/")).length);
      var aux = $location.path().substr(0, $location.path().lastIndexOf("/"));
      return ( ($location.path() === path) || (aux  === path && path != '/dashboard')) ? 'active' : '';
    }

  }
})();
