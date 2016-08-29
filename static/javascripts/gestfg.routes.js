(function () {
  'use strict';

  angular
    .module('gestfg.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/register', {
      controller: 'RegisterController',
      controllerAs: 'registerCtrl',
      templateUrl: '/static/templates/authentication/register.html'
    })

    .when('/login', {
      controller: 'LoginController',
      controllerAs: 'loginCtrl',
      templateUrl: '/static/templates/authentication/login.html'
    })

    .when('/recover-password', {
      controller: 'RegisterController',
      controllerAs: 'registerCtrl',
      templateUrl: '/static/templates/authentication/recover-password.html'
    })

    .when('/reset-password', {
      controller: 'RegisterController',
      controllerAs: 'registerCtrl',
      templateUrl: '/static/templates/authentication/set-password.html'
    })

    .when('/tfgs', {
      controller: 'TfgsController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/tfgs.html'
    })

    .when('/dashboard', {
      controller: 'DashboardController',
      controllerAs: 'dashCtrl',
      templateUrl: '/static/templates/layout/dashboard.html'
    })

    .when('/dashboard/usuarios', {
      controller: 'UsersController',
      controllerAs: 'usersCtrl',
      templateUrl: '/static/templates/layout/dashboard/users/users.html'
    })
    .when('/dashboard/usuarios/add', {
      controller: 'NewUserController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/users/add-user.html'
    })

    .when('/dashboard/tfgs', {
      controller: 'TfgsController',
      controllerAs: 'tfgsCtrl',
      templateUrl: '/static/templates/layout/dashboard/tfgs/tfgs.html'
    })
    .when('/dashboard/tfgs-asig', {
      controller: 'TfgsController',
      controllerAs: 'tfgsCtrl',
      templateUrl: '/static/templates/layout/dashboard/tfgs/tfgs-asig.html'
    })
    .when('/dashboard/tfgs/add', {
      controller: 'NewTfgController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/tfgs/add-tfg.html'
    })
    .when('/dashboard/tfgs/validate:datos', {
      controller: 'UploadTfgsController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/tfgs/validate-tfgs.html'
    })

    .when('/dashboard/departamentos', {
      templateUrl: '/static/templates/layout/dashboard/departamentos/departamentos.html'
    })
    .when('/dashboard/departamentos/add', {
      controller: 'NewDepartamentoController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/departamentos/add-departamento.html'
    })

    .when('/dashboard/eventos', {
      templateUrl: '/static/templates/layout/dashboard/events/events.html'
    })
    .when('/dashboard/eventos/add', {
      controller: 'NewEventController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/events/add-event.html'
    })

    .when('/dashboard/comisiones', {
      controller: 'ComisionesController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/comisiones/comisiones.html'
    })

    .when('/dashboard/tribunales', {
      templateUrl: '/static/templates/layout/dashboard/tribunales/tribunales.html'
    })

    .when('/dashboard/tfgs/upload', {
      templateUrl: '/static/templates/layout/dashboard/tfgs/upload-tfgs.html'
    })

    .when('/dashboard/upload', {
      controller: 'DashboardController',
      controllerAs: 'dashCtrl',
      templateUrl: '/static/templates/layout/dashboard/upload.html'
    })

    .when('/dashboard/calendar', {
      templateUrl: '/static/templates/layout/dashboard/calendar/calendar.html'
    })

    .when('/', {
      controller: 'IndexController',
      controllerAs: 'indexCtrl',
      templateUrl: '/static/templates/layout/index.html'
    })

    .otherwise('/');
  }
})();
