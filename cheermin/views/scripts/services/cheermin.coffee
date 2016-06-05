'use strict'

###*
 # @ngdoc service
 # @name cheerminWebappApp.cheermin
 # @description
 # # cheermin
 # Service in the cheerminWebappApp.
###
angular.module 'cheerminServices', ['ngResource']
  .factory 'Athletes', ['$resource', ($resource) ->
    return $resource '/rest/api/1/athletes/:athleteId', {}, {
      query: {method: 'GET', params: {athleteId: ''}, isArray:true}
    }
  ]
