/**
 * Created by hyt on 16-5-8.
 */
/**
 * Created by hyt on 16-5-7.
 */
var app=angular.module('monitor',[])
app.controller('monitorController',['$scope','$http',function($scope,$http){
    $scope.msg="hello word!";
    $http.get("http://monitor.hudieshanfood.com/network/status")
        .success(function(response){
            $scope.hostList=response.networks['192.168.20.1/24'];
        })
}])
