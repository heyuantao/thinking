/**
 * Created by hyt on 16-5-8.
 */
var app=angular.module('monitor.network',[])
app.controller('monitor.networkController',['$scope','$http','networkService',function($scope,$http,networkService){
    $scope.msg="hello";
    $scope.networkList=[];
    $scope.selectedNetwork="";
    $scope.hostList=[];
    networkService.networkList()
        .then(function(response){
            $scope.networkList=response;
        })
    $scope.$watch('selectedNetwork',function(value){
        networkService.networkStatus(value)
            .then(function(response){
                $scope.hostList=response;
            })
    })
}])

app.filter('portFilter',function(){
    return function(value){
        if(value>0){
            return "在线"
        }else{
            return "离线"
        }
    }
});