app.controller('ShareController', ['$scope','$http','$location', function($scope,$http,$location){
	
	if(localStorage.userID == null){
		$location.url("/")
	}

	$scope.send = function(){
		config = {

			headers:{'Accept': "json",
			"Authorization":"Basic " +localStorage.token

			}
	}

	$http.get('/api/send/'+localStorage.userID+'/'+$scope.email, config).then(function(response){
		console.log(response)
	})
	}

	
}])