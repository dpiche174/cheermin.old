'use strict'

###*
 # @ngdoc overview
 # @name cheerminWebappApp
 # @description
 # # cheerminWebappApp
 #
 # Main module of the application.
###
angular
  .module 'cheermin', [
    # 'ngAnimate',
    # 'ngCookies',
    'ngResource',
    'ngRoute',
    'cheerminServices',
    # 'ngSanitize',
    # 'ngTouch'
  ]
  .config ($routeProvider, $locationProvider) ->
    $routeProvider
      .when '/',
        templateUrl:  '/static/views/attendance.html'
        controller:   'AttendanceController'
        controllerAs: 'attendance'
      .otherwise
        redirectTo: '/'
    $locationProvider.html5Mode true

  # Application Controller
  .controller 'ApplicationController', ($scope, $route, $routeParams, $location) ->
      $scope.$route = $route
      $scope.$location = $location
      $scope.$routeParams = $routeParams

      $scope.isActive = (viewLocation) ->
        return viewLocation == $location.path()
