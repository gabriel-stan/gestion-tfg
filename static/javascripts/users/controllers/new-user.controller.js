/**
* NewUserController
* @namespace gestfg.users.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.users.controllers')
    .controller('NewUserController', NewUserController);

  NewUserController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Users'];

  /**
  * @namespace NewUserController
  */
  function NewUserController($rootScope, $scope, Authentication, Snackbar, Users) {
    var newUserCtrl = this;

    newUserCtrl.submit = submit;

    /**
    * @name submit
    * @desc Create a new User
    * @memberOf gestfg.users.controllers.NewUserController
    */
    function submit() {

      $rootScope.$broadcast('user.created', {
        first_name: newUserCtrl.user.first_name,
        last_name: newUserCtrl.user.last_name,
        clase: newUserCtrl.user.clase,
        is_admin: newUserCtrl.user.is_admin,
        email: newUserCtrl.user.email,
        departamento: newUserCtrl.user.departamento,
        created_at: newUserCtrl.created_at
      });

      // $scope.closeThisDialog();

      Users.create(newUserCtrl.user).then(createUserSuccessFn, createUserErrorFn);


      /**
      * @name createUserSuccessFn
      * @desc Show snackbar with success message
      */
      function createUserSuccessFn(data, status, headers, config) {
        Snackbar.success('El usuario se ha creado con éxito.');
      }


      /**
      * @name createUserErrorFn
      * @desc Propagate error event and show snackbar with error message
      */
      function createUserErrorFn(data, status, headers, config) {
        $rootScope.$broadcast('user.created.error');
        Snackbar.error(data.message);
      }
    }
  }
})();
