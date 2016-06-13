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

    .when('/dashboard/tfg', {
      templateUrl: '/static/templates/layout/dashboard/tfg/tfgs.html'
    })

    .when('/dashboard/departamentos', {
      templateUrl: '/static/templates/layout/dashboard/departamentos/departamentos.html'
    })

    .when('/dashboard/eventos', {
      templateUrl: '/static/templates/layout/dashboard/events/events.html'
    })
    .when('/dashboard/eventos/add', {
      controller: 'NewEventController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/dashboard/events/add-event.html'
    })

    .when('/dashboard/tfg/upload', {
      templateUrl: '/static/templates/layout/dashboard/tfg/upload-tfgs.html'
    })

    .when('/', {
      controller: 'IndexController',
      controllerAs: 'indexCtrl',
      templateUrl: '/static/templates/layout/index.html'
    })

    .otherwise('/');
  }
})();
