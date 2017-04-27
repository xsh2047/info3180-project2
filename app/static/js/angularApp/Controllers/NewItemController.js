app.controller('NewItemController', ['$scope','$http','$location',function($scope,$http,$location){
	if(localStorage.userID == null){
		$location.url("/")
	}

	$scope.url = ""
	$scope.addItem = function(){
		config ={

			headers:{'Accept': "json"}
		}
		console.log("adding")
		$http.get('/api/thumbnails?url='+$scope.url, config).then(function(response){
			console.log(response.data)
		})
	}
}])