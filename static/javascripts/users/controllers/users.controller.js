/**
* UsersController
* @namespace gestfg.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.controllers')
    .controller('UsersController', UsersController);

  UsersController.$inject = ['$scope'];

  /**
  * @namespace UsersController
  */
  function UsersController($scope) {

    var usersCtrl = this;
    usersCtrl.loadUsers = loadUsers;

    /**
    * @name loadUsers
    * @desc Loads all users from database
    * @memberOf gestfg.users.controllers.UsersController
    */
    function loadUsers(){
      // alert("Load users controlador");
    }

    // $scope.loadUsers = function() {
    //   alert("Cargando usuarios scope");
    // }


  }
})();
