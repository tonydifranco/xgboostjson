var http = require('http');
var url = require('url');
var fs = require('fs');
var spawn = require('child_process').spawn;
var model = require('./model.js');
http.createServer(function(request, response){
	var q = url.parse(request.url, true).query;
	if(Object.keys(q) == 0){
		fs.readFile('./demo.html', function(error, data){
			response.end(data, 'utf-8');
		});
	}else{
		if(q.method == 'node'){
			delete q.method;
			response.end(model.predict(q).toFixed(3), 'utf-8');
		}else{
			delete q.method;
			var RCall = ['--vanilla', 'R/child_process.R', JSON.stringify(q)];
			var R = spawn("Rscript", RCall, {cwd: '.', env: process.env})
			R.stdout.on("data", function(data){
				response.end(data, 'utf-8');
			});
		}
	}
}).listen(8080);