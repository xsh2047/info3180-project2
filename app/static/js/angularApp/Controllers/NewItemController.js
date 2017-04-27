app.controller('NewItemController', ['$scope','$http','$location',function($scope,$http,$location){
	if(localStorage.userID == null){
		$location.url("/")
	}

	$scope.url = ""
	$scope.thumbList=[]
	$scope.showThumbs = false
	
	$scope.addItem = function(){
		config ={

			headers:{
				'Accept': "json",
				"Authorization":"Basic "+localStorage.token
			}
		}
		console.log("adding")

		$http.get('/api/thumbnails?url='+$scope.url, config).then(function(response){
			$scope.thumbList = response.data.data.thumbnails
			$scope.showThumbs = true
			console.log($scope.thumbList)
		})
	}

	$scope.select = function(v){
		$scope.thumbnail = $scope.thumbList[v]
		config = {

			headers:{'Content-Type': "json",
			"Authorization":"Basic " +localStorage.token

			}
		}

		data = {
			"name": $scope.name,
			"thumbnail":$scope.thumbnail,
			"url":$scope.url,
			"desc":$scope.description
		}

	$http.post('/api/users/'+localStorage.userID+'/wishlist',data, config).then(function(response){
		
			if(response.data.message =="Success"){
				console.log(response.data.message)
				$location.url('/wishlist')
			}else{
				console.log(response.data.message)
			}
			
	
	})
	}
}])