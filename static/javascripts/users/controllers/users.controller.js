/**
* UsersController
* @namespace gestfg.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.controllers')
    .controller('UsersController', UsersController);

  UsersController.$inject = ['$scope', '$document'];

  /**
  * @namespace UsersController
  */
  function UsersController($scope, $document) {

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

    $scope.loadSelectedUser = function() {
      var user = $("#tabla-users").DataTable().row( { selected: true } ).data();
      $scope.selectedUser.first_name = user.first_name;
      $scope.selectedUser.last_name = user.last_name;
      $scope.selectedUser.email = user.email;
      $scope.selectedUser.departamento = user.departamento;
      $scope.selectedUser.tipo = user.clase;
      $scope.selectedUser.is_admin = user.is_admin;
    }

    $scope.selectedUser = new Object();


    $document.on('/dashboard/usuarios', function(event){
      $document.off('/dashboard/usuarios');
      $document.trigger('ready');
    });

  }
})();
