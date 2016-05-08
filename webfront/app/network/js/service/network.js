/**
 * Created by hyt on 16-5-8.
 */
var app=angular.module('monitor.network')
app.factory('networkService',['$http','$q',function($http,$q){
    var network_status_url="http://monitor.hudieshanfood.com/network/status";
    var network_list_url="http://monitor.hudieshanfood.com/network/network/list";
    var service={
        networkStatus:function(oneNetwork){
            var deferred = $q.defer();
            $http.get(network_status_url)
                .success(function(data,status){
                    statusInformation=data['networks']
                    oneStatusInformation=statusInformation[oneNetwork]
                    deferred.resolve(oneStatusInformation);
                })
                .error(function(data,status){
                    deferred.resolve(data);
                })
            return deferred.promise;
        },
        networkList:function(){
            var deferred = $q.defer();
            $http.get(network_list_url)
                .success(function(data,status){
                    statusInformation=data['networks']
                    deferred.resolve(statusInformation);
                })
                .error(function(data,status){
                    deferred.resolve(data);
                })
            return deferred.promise;
        }
    }
    return service;
}])