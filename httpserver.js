var http = require('http');
var url = require('url');
var fs = require('fs');
var spawn = require('child_process').spawn;
var model = require('./R/model.js');
// or
// var model = require('./python/model.js');
http.createServer(function(request, response){
	var q = url.parse(request.url, true).query;
	if(Object.keys(q) == 0){
		fs.readFile('./demo.html', function(error, data){
			response.end(data, 'utf-8');
		});
	}else{
		var method = q.method;
		delete q.method;
		if(method == 'node'){
			response.end(model.predict(q).toFixed(3), 'utf-8');
		}else if(method == 'r'){
			var RCall = ['--vanilla', 'R/child_process.R', JSON.stringify(q)];
			var R = spawn("Rscript", RCall, {cwd: '.', env: process.env})
			R.stdout.on("data", function(data){
				response.end(data, 'utf-8');
			});
		}else if(method == 'python'){
			var pyCall = ['python/child_process.py', JSON.stringify(q)];
			var python = spawn("python", pyCall, {cwd: '.', env: process.env})
			python.stdout.on("data", function(data){
				response.end(data, 'utf-8');
			});
		}else{
			resonse.writeHead(500).end('error!');
		}
	}
}).listen(8080);