/**
* DashboardController
* @namespace gestfg.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('gestfg.layout.controllers')
    .controller('DashboardController', DashboardController);

  DashboardController.$inject = ['$scope', 'Authentication', 'Events', 'Snackbar', 'Dashboard', 'Departamentos'];

  /**
  * @namespace DashboardController
  */
  function DashboardController($scope, Authentication, Events, Snackbar, Dashboard, Departamentos) {
    var dashCtrl = this;

    dashCtrl.events = [];
    dashCtrl.departamentos = [];
    dashCtrl.upload = upload;

    dashCtrl.tipos_evento =
    {
        "status": true,
        "data": [
            {
                "id": 1,
                "codigo": "CONV_JUN",
                "nombre": "Convocatoria de Junio"
            },
            {
                "id": 2,
                "codigo": "CONV_SEPT",
                "nombre": "Convocatoria de Septiembre"
            },
            {
                "id": 3,
                "codigo": "CONV_DIC",
                "nombre": "Convocatoria de Diciembre"
            },
            {
                "id": 4,
                "codigo": "INFOR",
                "nombre": "Informativo"
            }
        ]
    };

    dashCtrl.subtipos_evento =
    {
        "data": [
            {
                "codigo": "ASIG_TFG",
                "nombre": "Asignación TFG"
            },
            {
                "codigo": "SOL_EVAL",
                "nombre": "Notificación Solicitud de Evaluación"
            },
            {
                "codigo": "COM_EVAL",
                "nombre": "Establecimiento de las Comisiones de Evaluación"
            },
            {
                "codigo": "ENT_MAT",
                "nombre": "Entrega de material"
            },
            {
                "codigo": "ENT_INF_TUTOR",
                "nombre": "Entrega del Informe del Tutor"
            },
            {
                "codigo": "DEF_TFG",
                "nombre": "Defensa del TFG"
            },
            {
                "codigo": "EVAL_TFG",
                "nombre": "Evaluación del TFG y Notificación al Centro"
            }
        ]
    };

    dashCtrl.titulaciones =
    {
        "data": [
            {
                "id": 1,
                "codigo": "GII",
                "nombre": "Grado en Ingeniería Informática"
            },
            {
                "id": 2,
                "codigo": "GIM",
                "nombre": "Doble Grado en Ingeniería Informática y en Matemáticas"
            },
            {
                "id": 3,
                "codigo": "GITT",
                "nombre": "Grado en Ingeniería de Tecnologías de Telecomunicación"
            },
            {
                "id": 4,
                "codigo": "MPII",
                "nombre": "Máster Profesional en Ingeniería Informática"
            },
            {
                "id": 5,
                "codigo": "MPIT",
                "nombre": "Máster Profesional en Ingeniería de Telecomunicación"
            }
        ]
    };

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf gestfg.layout.controllers.DashboardController
    */
    function activate() {

      // cargar datos de relleno para la demo TODO quitar cuando no nos haga falta en el dashboard
      try {
        var s = document.createElement('script'); // use global document since Angular's $document is weak
        s.src = 'static/dist/js/pages/dashboard2.js';
        document.body.appendChild(s);
      } catch (e) {
        console.log(e);
      }

      Departamentos.all().then(dptSuccessFn, dptErrorFn);

      /**
      * @name eventsSuccessFn
      * @desc Update events array on view
      */
      function dptSuccessFn(data, status, headers, config) {
        dashCtrl.departamentos = data.data.data;
      }


      /**
      * @name eventsErrorFn
      * @desc Show snackbar with error
      */
      function dptErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }

      Events.all().then(eventsSuccessFn, eventsErrorFn);
      //
      // $scope.$on('event.created', function (event, ev) {
      //   dashCtrl.events.unshift(ev);
      // });
      //
      // $scope.$on('event.created.error', function () {
      //   dashCtrl.events.shift();
      // });


      /**
      * @name eventsSuccessFn
      * @desc Update events array on view
      */
      function eventsSuccessFn(data, status, headers, config) {
        dashCtrl.events = data.data.data;
      }


      /**
      * @name eventsErrorFn
      * @desc Show snackbar with error
      */
      function eventsErrorFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }
    }


    function upload(){
      var fd = new FormData();

      var f = document.getElementById('upload-file').files[0];

      fd.append('file', f);
      fd.append('model', dashCtrl.up.model);

      Dashboard.upload(fd).then(uploadSuccessFn, uploadErrorFn);


      function uploadSuccessFn(data, status, headers, config) {
        Snackbar.success("Subida realizada correctamente");
      }

      function uploadErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.message);
      }

      // var r = new FileReader();
      // r.onloadend = function(e){
      //   var data = e.target.result;
      //   dashCtrl.up.file = data;
      //   send you binary data via $http or $resource or do anything else with it
      // }
      // r.readAsBinaryString(f);
    }
  }
})();
